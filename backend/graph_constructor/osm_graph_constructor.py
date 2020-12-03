import os
import pickle
from collections import defaultdict
import networkx as nx
import numpy as np

from graph_constructor.osm_graph import OsmGraph
from graph_constructor.graph_constructor import GraphConstructor
from graph_constructor.tags import constraints_tags, ATTRACTION_TAG
from ml_module.clustering_model import ClusteringModel

MAX_DIST = 2_000
INF_DIST = 1_000_000

AVERAGE_RATE = 1.5


class OsmGraphConstructor(GraphConstructor):

    def __init__(self, data_processor, cdir, cache=True):
        super().__init__()
        self.cdir = cdir
        self.cache = cache
        self.data_processor = data_processor
        if not os.path.isdir(cdir):
            os.mkdir(cdir)

    def create_graph(self, params, max_points=None, city=None):
        """
        Создание OsmGraph вокруг стартовой точки.

        Params:
             params(dict) - параметры с ограничениями для маршрута. Ключи:
                'start_lat'(float) - широта стартовой точки.
                'start_lng'(float) - долгота стартовой точки.
                'distance' (int) - максимальный путь, который пройдет человек.
                'tags' (list) - спиок тэгов.
            max_points(int) - максимальное кол-во poi в одной категории.
            city(str) - город, для загрузки графа из cash.

        Returns:
            osm_graph
        """
        lat = params.get('start_lat')
        lon = params.get('start_lng')
        dist = params.get('distance')
        key = f'{lat}_{lon}_{dist}'
        fnam = os.path.join(self.cdir, f'osm_graph_{key}.pkl')
        if self.cache and os.path.isfile(fnam):
            return OsmGraph.load(fnam)
        else:
            fcity = os.path.join(self.cdir, f'{city}.pkl')
            if city is not None and os.path.isfile(fcity):
                with open(fcity, 'rb') as f:
                    graph, path = pickle.load(f)
            else:
                graph = nx.Graph()
                path = defaultdict(lambda: {})
                ways = self._find_way(lat, lon, dist)
                for way in ways:
                    way_nd = way['simple_nodes']
                    graph.add_weighted_edges_from(zip(way_nd[:-1], way_nd[1:], way['length']))
                    for k, v, w in zip(way_nd[:-1], way_nd[1:], way['simple_way']):
                        path[k][v] = w
                        path[v][k] = list(reversed(w))
                path = dict(path)
                Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
                graph = graph.subgraph(Gcc[0]).copy()
            data = self._create_data(graph, params, max_points)
            osm_graph = OsmGraph(graph, path, data)
            if self.cache:
                osm_graph.save(fnam)
            return osm_graph

    def _find_way(self, lat, lon, dist):
        """
        Поиск дорог в заданной окружности.

        Args:
            lat(float) - широта.
            lon(float) - долгота.
            dist(float) - радиус поиска в метрах.

        Returns:
            list - список найденных дорог.
        """
        return self.data_processor.select_query('ways', {'road': True,
                                                         'location': {'$near': {'$geometry': {'type': 'LineString',
                                                                                              'coordinates': [lon,
                                                                                                              lat]},
                                                                                '$maxDistance': dist}}})

    def _create_data(self, graph, params, max_points):
        """
        Создание словаря с информацией о poi.

        Args:
            graph(networkx.Graph): - граф, в состав которого входят poi.
            params(dict) - параметры с ограничениями для маршрута.
            max_points(int) - максимальное кол-во poi в одной категории.

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
                distance_matrix(list) - матрица кратчайших расстояний(int), размером (nv, nv)
                rewards(list) - список наград для точек интереса.
        """
        poi = self._find_poi(graph, params, max_points)
        points = poi['points']
        start_point = self._find_node(graph, params)
        try:
            length, path = nx.single_source_dijkstra(graph, start_point['id_osm'], cutoff=MAX_DIST)
        except nx.NetworkXNoPath:
            length = {}
        start_dist = [length.get(nd['id_osm'], INF_DIST) for nd in points] + [0]
        distance_matrix = [[i['dist_matrix'].get(j['id_osm'], INF_DIST) for j in points] + [start_dist[k]]
                           for k, i in enumerate(points)] + [start_dist]

        points.append(start_point)
        return {
            'ids': [i['id_osm'] for i in points],
            'category': poi['category'] + ['start_point'],
            'locations': [[i['location']['coordinates'][x] for x in [1, 0]] for i in points],
            'nv': len(points),
            'num_vehicles': 1,
            'depot': len(points) - 1,
            'constraints': poi['constraints'],
            'distance_matrix': distance_matrix,
            'rewards': poi['rewards'] + [0]
        }

    def _find_node(self, graph, params):
        """
        Поиск точки из графа, ближайшей к стартовой.

        Args:
            graph(networkx.Graph): - граф, в состав которого должна попадать найденная точка.
            params(dict) - параметры с ограничениями для поиска точки.

        Returns:
            node - найденный элемент из mongo.
        """
        nodes = self.data_processor.get_nearest_points(params['start_lat'], params['start_lng'],
                                                       params['distance'])
        nodes = [node for node in nodes if node['id_osm'] in graph.nodes()]
        if len(nodes) > 0:
            return nodes[0]
        return None

    def _find_poi(self, graph, params, max_points):
        """
        Поиск poi из графа, ближайших к стартовой точке.

        Args:
            graph(networkx.Graph): - граф, в состав которого должны попадать найденные poi.
            params(dict) - параметры с ограничениями для поиска точки.
            max_points(int) - максимальное кол-во poi в одной категории.

        Returns:
            dict - найденные poi и их свойства. Ключи:
                points(list) - найденные элементы из mongo.
                category(list) - категория найденных poi.
                constraints(dict) - словарь constraints с индексами(в points):
                        {category_constraint: [], ...}
        """
        global_tags = [constraints_tags.get(tag) for tag in params['tags']]
        poi = {'points': [],
               'category': [],
               'rewards': [],
               'constraints': {}}
        points = self.data_processor.select_query('poi', {
            'global_tags': {'$in': params['tags']},
            'location': {
                '$near': {'$geometry': {'type': 'Point',
                                        'coordinates': [params['start_lng'], params['start_lat']]},
                          '$maxDistance': params['distance']}}})
        points = [node for node in points if node['id_osm'] in graph.nodes()]

        for global_tag in set(global_tags):
            tags_current = [i for i, j in zip(params['tags'], global_tags) if j == global_tag]
            poi_current = [node for node in points if
                           len([1 for tag in tags_current if tag in node['global_tags']]) > 0]
            if global_tag is not None:
                if max_points is not None and len(poi_current) > max_points:
                    poi_current = self._add_poi_rewards(poi_current, global_tag)
                    poi_current = self._clustering(poi_current, max_points)
                poi['constraints'][global_tag] = list(range(len(poi['points']), len(poi['points']) + len(poi_current)))
            else:
                poi_current = poi_current[:max_points]
                poi_current = self._add_poi_rewards(poi_current, ATTRACTION_TAG)
            poi['category'] += [global_tag if global_tag is not None else ATTRACTION_TAG] * len(poi_current)
            poi['points'] += poi_current
            poi['rewards'] += [node['reward'] for node in poi_current]

        return poi

    @staticmethod
    def _clustering(poi, n_clusters):
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
    def _add_poi_rewards(points, category):
        """
        Добавление наград к точкам интереса.

        Args:
            points(list) - точки интереса из mongo.
            category(str) - категория всех точек интереса.

        Returns:
            points(list) - точки интереса с аттрибутами `reward` (награда в каждой точке).
        """
        def get_centralities(points):
            ids = [p['id_osm'] for p in points]
            centralities = np.array(
                [1.0 / np.nanmean([p['dist_matrix'].get(node2, np.nan) for node2 in ids if p['id_osm'] != node2]) for p
                 in points])
            finite_nums = np.isfinite(centralities)
            centralities[~finite_nums] = np.max(centralities[finite_nums])
            min_centrality = np.min(centralities)
            max_centrality = np.max(centralities)
            centralities = 3.0 * (centralities - min_centrality) / (max_centrality - min_centrality)
            return centralities

        rewards = np.array([p['rate'] if 'rate' in p else np.nan for p in points])

        if category != ATTRACTION_TAG:
            centralities = get_centralities(points)
            rewards = np.array([centralities[i] if np.isnan(rewards[i]) else max(rewards[i], centralities[i]) for i in
                                range(len(points))])

        if np.count_nonzero(~np.isnan(rewards)):
            rewards[np.isnan(rewards)] = max(np.nanmean(rewards), AVERAGE_RATE)
        else:
            rewards[np.isnan(rewards)] = 1

        rewards = (10 * rewards).astype(int)
        rewards[rewards == 0] = 1
        for i, node in enumerate(points):
            node['reward'] = rewards[i]
        return points
