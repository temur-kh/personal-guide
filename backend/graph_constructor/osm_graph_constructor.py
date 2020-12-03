import os
import pickle
from collections import defaultdict
import networkx as nx
import numpy as np

from graph_constructor.osm_graph import OsmGraph
from graph_constructor.graph_constructor import GraphConstructor
from graph_constructor.tags import constraints_tags, all_tags, ATTRACTION_TAG
from ml_module.clustering_model import ClusteringModel

MAX_DIST = 2_000
INF_DIST = 1_000_000

AVERAGE_RATE = 1.5


class OsmGraphConstructor(GraphConstructor):

    def __init__(self, data_processor, cdir, cities, cache=True):
        super().__init__()
        self.cdir = cdir
        self.cache = cache
        self.data_processor = data_processor
        self.cities = cities
        if not os.path.isdir(cdir):
            os.mkdir(cdir)

    @staticmethod
    def create(data_processor, cdir, cache=True):
        cities = {}
        city_dir = cdir + '/cities'
        files = os.listdir(path=city_dir)
        for file in files:
            city = file.split('.')[0]
            fcity = os.path.join(city_dir, file)
            with open(fcity, 'rb') as f:
                graph_poi, graph, path = pickle.load(f)
            cities[city] = {'graph_poi': graph_poi,
                            'graph': graph,
                            'path': path}

        return OsmGraphConstructor(data_processor, cdir, cities, cache=cache)

    def create_graph(self, params, max_points=None):
        """
        Создание OsmGraph вокруг стартовой точки.

        Params:
             params(dict) - параметры с ограничениями для маршрута. Ключи:
                'start_lat'(float) - широта стартовой точки.
                'start_lng'(float) - долгота стартовой точки.
                'distance' (int) - максимальный путь, который пройдет человек.
                'tags' (list) - спиок тэгов.
            max_points(int) - максимальное кол-во poi в одной категории constraint.

        Returns:
            osm_graph
        """
        params['start_point'] = self._find_node(params)
        city = params['start_point'].get('city')

        coord = self._get_coord(params['start_point'])
        key = "_".join((str(coord),
                        str(params['distance']),
                        str(params['tags'])))
        fnam = os.path.join(self.cdir, f'osm_graph_{key}.pkl')
        if self.cache and os.path.isfile(fnam):
            return OsmGraph.load(fnam)
        else:
            if self.cities.get(city) is not None:
                graph_poi, graph, path = self.cities[city].values()
                start = params['start_point']['id_osm']
                if start not in graph_poi.nodes():
                    try:
                        length = nx.single_source_dijkstra_path_length(graph, start, cutoff=MAX_DIST)
                    except nx.NetworkXNoPath:
                        length = {}
                    add_edges = [(start, end, weight) for end, weight in length.items() if end in graph_poi.nodes()]
                    if len(add_edges) > 0:
                        graph_poi.add_weighted_edges_from(add_edges)
            else:
                graph_poi = None
                graph = nx.Graph()
                ways = self._find_way(params)
                add_edges = [(way['start'], way['end'], way['length']) for way in ways]
                graph.add_weighted_edges_from(add_edges)
                path = defaultdict(lambda: {})
                for way in ways:
                    path[way['start']][way['end']] = way['simple_way']
                    path[way['end']][way['start']] = list(reversed(way['simple_way']))
                path = dict(path)
                Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
                graph = graph.subgraph(Gcc[0]).copy()
            data = self._create_data(params, graph, graph_poi=graph_poi, max_points=max_points)
            osm_graph = OsmGraph(graph, path, data)
            if self.cache:
                osm_graph.save(fnam)
            return osm_graph

    def _create_data(self, params, graph, graph_poi=None, max_points=None):
        """
        Создание словаря с информацией о poi.

        Args:
            graph(networkx.Graph): - граф, в состав которого входят poi.
            params(dict) - параметры с ограничениями для маршрута.
            max_points(int) - максимальное кол-во poi в одной категории constraint.

        Returns:
            data(dict) - информациея о poi. Ключи:
                ids(list) - список id_osm.
                category(list) - список категорий poi.
                locations(list) - список координат poi в формате: [lat, lon].
                nv(int) - кол-во poi.
                num_vehicles(int)
                depot(int) - индекс(в ids) стартовой точки.
                constraints(dict) - словарь constraints с индексами(в ids):
                        {category_constraint: [], ...}
                distance_matrix(list) - матрица кратчайших расстояний(int), размером (nv, nv).
                rewards(list) - список наград для точек интереса.
        """
        poi = self._get_poi(graph_poi, params, max_points)
        points = poi['points'] + [params['start_point']]
        nv = len(points)
        distance_matrix = [[]] * nv
        if graph_poi is None:
            graph_poi = graph
        for i in range(nv):
            try:
                length = nx.single_source_dijkstra_path_length(graph_poi, points[i]['id_osm'], cutoff=MAX_DIST)
            except nx.NetworkXNoPath:
                length = {}
            distance_matrix[i] = [length.get(nd['id_osm'], INF_DIST) for nd in points]
        return {
            'ids': [i['id_osm'] for i in points],
            'category': poi['category'] + ['start_point'],
            'locations': [self._get_coord(i) for i in points],
            'nv': nv,
            'num_vehicles': 1,
            'depot': nv - 1,
            'constraints': poi['constraints'],
            'distance_matrix': distance_matrix,
            'rewards': poi['rewards'] + [0]
        }

    def _find_way(self, params):
        """
        Поиск дорог из графа, ближайших к стартовой точке.

        Args:
            params(dict) - параметры с ограничениями для маршрута.

        Returns:
            list - список найденных дорог.
        """
        coord = self._get_coord(params['start_point'], inverse=True)
        dist = params['distance']
        params = {'location': {'$near': {'$geometry': {'type': 'LineString',
                                                       'coordinates': coord},
                                         '$maxDistance': dist}}}
        return self.data_processor.select_query('ways_graph', params)

    def _find_node(self, params):
        """
        Поиск точки из графа, ближайшей к стартовой точке.

        Args:
            params(dict) - параметры с ограничениями для поиска точки.

        Returns:
            node - найденный элемент из mongo.
        """
        coord = [params['start_lng'], params['start_lat']]
        dist = params['distance']
        params = {'location': {'$near': {'$geometry': {'type': 'Point',
                                                       'coordinates': coord},
                                         '$maxDistance': dist}}}
        nodes = self.data_processor.select_query('nodes_graph', params, limit_number=1)
        if len(nodes) > 0:
            return nodes[0]

        return {}

    def _find_poi(self, params):
        """
        Поиск poi из графа, ближайших к стартовой точке.

        Args:
            params(dict) - параметры с ограничениями для поиска точки.

        Returns:
            list - список найденных poi.
        """
        coord = self._get_coord(params['start_point'], inverse=True)
        dist = params['distance']
        tags = params['tags']
        params = {'global_tags': {'$in': tags},
                  'location': {'$near': {'$geometry': {'type': 'Point',
                                                       'coordinates': coord},
                                         '$maxDistance': dist}}}
        return self.data_processor.select_query('poi', params)

    def _get_poi(self, graph_poi, params, max_points):
        """
        Получение свойств poi, ближайших к стартовой точке.

        Args:
            graph(networkx.Graph): - граф, в состав которого должны попадать найденные poi.
            params(dict) - параметры с ограничениями для поиска точки.
            max_points(int) - максимальное кол-во poi в одной категории constraint.

        Returns:
            dict - найденные poi и их свойства. Ключи:
                points(list) - найденные элементы из mongo.
                category(list) - категория найденных poi.
                rewards(list) - список наград для poi.
                constraints(dict) - словарь constraints с индексами(в points):
                        {category_constraint: [], ...}
        """
        poi = {'points': [],
               'category': [],
               'rewards': [],
               'constraints': {}}
        points = self._find_poi(params)
        points = [node for node in points if node['id_osm'] in graph_poi.nodes()]

        global_tags = [all_tags.get(tag) for tag in params['tags']]
        for global_tag in set(global_tags):
            tags = [i for i, j in zip(params['tags'], global_tags) if j == global_tag]
            poi_tag = [node for node in points
                       if len(set(tags) & set(node['global_tags'])) > 0]
            num_poi_tag = len(poi_tag)
            if global_tag in constraints_tags:
                poi_tag = self._add_poi_rewards(graph_poi, poi_tag, global_tag)
                if max_points is not None and len(poi_tag) > max_points:
                    poi_tag = self._clustering(poi_tag, max_points)
                num_point = len(poi['points'])
                poi['constraints'][global_tag] = list(range(num_point, num_point + num_poi_tag))
            else:
                poi_tag = poi_tag[:max_points]
                poi_tag = self._add_poi_rewards(graph_poi, poi_tag, ATTRACTION_TAG)
            poi['category'] += [global_tag] * num_poi_tag
            poi['points'] += poi_tag
            poi['rewards'] += [node['reward'] for node in poi_tag]
        return poi

    def _clustering(self, poi, n_clusters):
        """
        Классификация poi по карте и выбор максимального reward в кластере.

        Args:
            poi(list) - точки интереса из mongo.
            n_clusters(int) - количество кластеров.

        Returns:
            list - точки интереса с максимальным reward в своем кластере.
        """
        clustering_model = ClusteringModel(params={'n_clusters': n_clusters})
        labels = clustering_model.fit_predict([nd['location']['coordinates'] for nd in poi])
        rewards = [node['reward'] for node in poi]

        order = np.lexsort((rewards, labels))
        idx = np.array([nd['id_osm'] for nd in poi])[order]
        labels = labels[order]

        index = np.empty(len(labels), 'bool')
        index[-1] = True
        index[:-1] = labels[1:] != labels[:-1]
        best_poi = [node for node in poi if node['id_osm'] in idx[index]]
        return best_poi

    @staticmethod
    def _get_coord(node, inverse=False):
        """
        Получение координат точки из mongo.

        Args:
            node(dict) - точка из mongo.
            inverse(bool) - при False возвращается [lat, lon], иначе наоборот.

        Returns:
            list - коорданаты точки.
        """
        coord = node['location']['coordinates']
        if inverse:
            return coord
        return [coord[1], coord[0]]

    @staticmethod
    def _add_poi_rewards(graph_poi, points, category):
        """
        Добавление наград к точкам интереса.
        Args:
            points(list) - точки интереса из mongo.
            category(str) - категория всех точек интереса.
        Returns:
            points(list) - точки интереса с аттрибутами `reward` (награда в каждой точке).
        """

        rewards = np.array([p['rate'] if 'rate' in p else np.nan for p in points])

        if category != ATTRACTION_TAG:
            centralities = np.array([graph_poi.nodes[p['id_osm']]['centrality'][category] for p in points])
            rewards = np.array([centralities[i] if np.isnan(rewards[i]) else max(rewards[i], centralities[i])
                                for i in range(len(points))])

        if np.count_nonzero(~np.isnan(rewards)):
            rewards[np.isnan(rewards)] = max(np.nanmean(rewards), AVERAGE_RATE)
        else:
            rewards[np.isnan(rewards)] = 1

        rewards = (10 * rewards).astype(int)
        rewards[rewards == 0] = 1
        for i, node in enumerate(points):
            node['reward'] = rewards[i]
        return points
