import os
import pickle
import networkx as nx
import numpy as np

from graph_constructor.Error import not_found_city, not_found_poi
from graph_constructor.osm_graph import OsmGraph
from graph_constructor.graph_constructor import GraphConstructor
from graph_constructor.starting_params import StartingParams
from graph_constructor.tags import *
from ml_module.clustering_model import ClusteringModel


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
                graph, path = pickle.load(f)
            cities[city] = {'graph': graph,
                            'path': path}
        return OsmGraphConstructor(data_processor, cdir, cities, cache=cache)

    def create_graph(self, start_params, max_points=None):
        """
        Создание OsmGraph вокруг стартовой точки.

        Params:
             start_params(dict) - параметры с ограничениями для маршрута. Ключи:
                'start_lat'(float) - широта стартовой точки.
                'start_lng'(float) - долгота стартовой точки.
                'distance' (int) - максимальный путь, который пройдет человек.
                'tags' (list) - спиок тэгов.
            max_points(int) - максимальное кол-во poi в одной категории constraint.

        Returns:
            osm_graph
        """
        params = StartingParams(start_params)
        start_point = self._find_node(params)
        if start_point is None:
            raise not_found_city()
        params.set_start_point(start_point)

        key = params.get_key()
        fnam = os.path.join(self.cdir, f'osm_graph_{key}.pkl')
        if self.cache and os.path.isfile(fnam):
            return OsmGraph.load(fnam)
        else:
            city = params.get_city()
            graph = self.cities[city]['graph'].copy()
            path = self.cities[city]['path']
            try:
                length = nx.single_source_dijkstra_path_length(graph, params.get_start_id(), cutoff=params.distance)
            except nx.NetworkXNoPath:
                raise not_found_poi()
            params.start_point['dist_matrix'] = length

            del_nodes = [nd for nd in graph.nodes() if nd not in length.keys()]
            graph.remove_nodes_from(del_nodes)

            poi = self._get_poi(graph, params, max_points)
            if len(poi['points']) == 1:
                return not_found_poi(self._get_available_tags(graph, params))
            osm_graph = OsmGraph.create(graph, path, poi, params)
            if self.cache:
                osm_graph.save(fnam)
            return osm_graph

    def _find_node(self, params):
        """
        Поиск точки из графа, ближайшей к стартовой точке.

        Args:
            params(StartingParams) - стартовые ограничения.

        Returns:
            node - найденный элемент из mongo.
        """
        query = {'location': {'$near': {'$geometry': {'type': 'Point',
                                                      'coordinates': params.start_coordinates},
                                        '$maxDistance': params.distance}}}
        nodes = self.data_processor.select_query('nodes_graph', query, limit_number=1)
        if len(nodes) > 0:
            return nodes[0]
        return None

    def _find_poi(self, params, points):
        """
        Поиск poi из графа, ближайших к стартовой точке.

        Args:
            params(StartingParams) - стартовые ограничения.
            points(list) - список id_osm, которые необходимо получить из mongo.

        Returns:
            list - список найденных poi.
        """
        query = {'city': params.get_city(), 'id_osm': {'$in': points}}
        return self.data_processor.select_query('poi', query)

    def _get_poi(self, graph, params: StartingParams, max_points):
        """
        Получение свойств poi, ближайших к стартовой точке.

        Args:
            params(StartingParams) - стартовые ограничения.
            max_points(int) - максимальное кол-во poi в одной категории constraint.

        Returns:
            dict - выбранные poi и их свойства. Ключи:
                points_id(list) - id выбранных poi.
                points(list) - элементы из mongo.
                category(list) - категория выбранных poi.
                constraints(dict) - словарь constraints с индексами(в points):
                        {category_constraint: [], ...}
        """
        poi = {'points_id': [],
               'category': [],
               'constraints': {}}
        for global_tag, tags in params.global_tags.items():
            poi_global_tag = list(nx.get_node_attributes(graph, global_tag).keys())
            poi_tag = [node for node in poi_global_tag if len(set(tags) & set(graph.nodes[node][global_tag])) > 0]
            rewards = np.array([graph.nodes[nd]['reward'][global_tag] for nd in poi_tag])
            if global_tag in constraints_tags:
                if max_points is not None and len(poi_tag) > max_points:
                    poi_tag = self._clustering(poi_tag, rewards, graph, max_points)
                poi['constraints'][global_tag] = list(
                    range(len(poi['points_id']), len(poi['points_id']) + len(poi_tag)))
            else:
                if max_points is not None and len(poi_tag) > max_points:
                    poi_tag = self._best_attraction(poi_tag, rewards, max_points)
            poi['category'] += [global_tag] * len(poi_tag)
            poi['points_id'] += poi_tag
        poi['points'] = self._find_poi(params, poi['points_id'])
        # добавление данных стартовой точки
        poi['points'].append(params.start_point)
        poi['points_id'].append(params.get_start_id())
        poi['category'].append(START_POINT_TAG)
        return poi

    @staticmethod
    def _clustering(poi, rewards, graph, n_clusters):
        """
        Классификация poi по карте и выбор максимального reward в кластере.

        Args:
            poi(list) - список id_osm из текущего тэга.
            rewards(list) - награды для poi.
            graph(networkx.Graph): - граф.
            n_clusters(int) - количество кластеров.

        Returns:
            list - точки интереса с максимальным reward в своем кластере.
        """
        clustering_model = ClusteringModel(params={'n_clusters': n_clusters})
        labels = clustering_model.fit_predict([graph.nodes[nd]['location'] for nd in poi])

        order = np.lexsort((rewards, labels))
        poi = np.array(poi)[order]
        labels = labels[order]

        index = np.empty(len(labels), 'bool')
        index[-1] = True
        index[:-1] = labels[1:] != labels[:-1]
        return list(poi[index])

    @staticmethod
    def _best_attraction(poi, rewards, max_points):
        """
        Классификация poi по карте и выбор максимального reward в кластере.

        Args:
            poi(list) - список id_osm из текущего тэга.
            rewards(list) - награды для poi.
            max_points(int) - минимальное количество элементов для отбора.

        Returns:
            list - точки интереса с максимальным reward.
        """
        order = np.argsort(rewards * -1)
        poi = list(np.array(poi)[order])
        rewards = rewards[order]
        add_point = (rewards[max_points:] == rewards[max_points - 1]).sum()
        return poi[:max_points + add_point]

    @staticmethod
    def _get_available_tags(graph, params):
        """
        Возвращает тэги достопримечательностей, которые есть в графе, помимо тех, что задал пользователь.
        Args:
            graph(networkx.Graph): - граф.
            params(StartingParams) - стартовые ограничения.

        Returns:
            list - список тэгов.
        """
        available_tags = []
        for global_tag in attractions_tags:
            poi_global_tag = list(nx.get_node_attributes(graph, global_tag).keys())
            if len(poi_global_tag) > 0:
                if global_tag in params.global_tags.keys():
                    tags = list(set([i for point in poi_global_tag
                                     for i in graph.nodes[point][global_tag] if i != global_tag]))
                    available_tags += tags
                else:
                    available_tags.append(global_tag)
        return available_tags
