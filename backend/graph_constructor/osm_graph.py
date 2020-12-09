import pickle
import networkx as nx

from graph_constructor.graph import Graph

INF_DIST = 1_000_000


class OsmGraph(Graph):
    def __init__(self, graph, way, data):
        """
        Params:
            graph(networkx.Graph) - граф вокруг стратовой точки.
            way(dict) - словарь путей между точками.
               {id_osm_start: {id_osm_end: [[lat, lon], ...], ...}, ...}
            data(dict) - информациея о poi. Ключи:
               ids(list) - список id_osm.
               category(list) - список категорий poi.
               locations(list) - список координат poi в формате: [lat, lon].
               nv(int) - количество poi.
               num_vehicles(int)
               depot(int) - индекс(в ids) стартовой точки.
               constraints(dict) - словарь constraints с индексами(в ids).
                       {category_constraint: [], ...}
               distance_matrix(list) - матрица кратчайших расстояний(int), размером (nv, nv).
               rewards(list) - список наград для точек интереса.
               stop_time(list) - список врмени остановки на poi.
               info(list) - список словарей с полями: description, photo
        """
        super().__init__()
        self.graph = graph
        self.way = way
        self.data = data

    def get_way(self, route):
        """
        Строит маршрут из результатов оптимайзера.

        Args:
            route(list) - путь на выходе из Optimizer (порядок обхода poi).

        Returns:
            points(list) - список словарей из локаций poi и их категорий, вида:
                lng(float) - долгота.
                lat(float) - широта.
                category(str) - категория poi.
            line_string(list) - список словарей из локаций всех точкек в маршруте в порядке обхода.
        """
        line_string = []
        points = []
        if len(self.data['ids']) > 0 and len(set(route)) > 1:
            for iv, jv in zip(route[:-1], route[1:]):
                points.append(self._poi_location(iv))
                length, path = nx.single_source_dijkstra(self.graph, self.data['ids'][iv], self.data['ids'][jv])
                for i, j in zip(path[:-1], path[1:]):
                    for line in self.way[i][j]:
                        line_string.append({'lng': line[1], 'lat': line[0]})
            points.append(self._poi_location(route[-1]))
        return points, line_string

    @staticmethod
    def create(graph, way, poi):
        """
        Args:
            graph(networkx.Graph) - граф вокруг стратовой точки.
            way(dict) - словарь путей между точками.
               {id_osm_start: {id_osm_end: [[lat, lon], ...], ...}, ...}
            poi(dict) - poi, которые войдут в data и их свойства. Ключи:
                points_id(list) - id выбранных poi.
                points(list) - элементы из mongo (порядок НЕ соответсвует points_id).
                category(list) - категория выбранных poi (порядок соответсвует points_id).
                constraints(dict) - словарь constraints с индексами(в points):
                        {category_constraint: [], ...}
        Returns:

        """
        dist_matrix = {nd['id_osm']: nd.get('dist_matrix') for nd in poi['points']}
        points_info = {nd['id_osm']: {'dist_matrix': nd.get('dist_matrix'),
                                      'description': nd.get('description'),
                                      'photo': nd.get('photo'),
                                      'name': nd.get('photo')} for nd in poi['points']}
        nv = len(poi['points_id'])
        distance_matrix = [[]] * nv
        for i in range(nv):
            length = dist_matrix[poi['points_id'][i]]
            distance_matrix[i] = [length.get(nd, INF_DIST) for nd in poi['points_id']]
        stop_time = [graph.nodes[nd].get('stop_time', {}).get(category, 0)
                     for nd, category in zip(poi['points_id'], poi['category'])]
        reward = [graph.nodes[nd].get('reward', {}).get(category, 0)
                  for nd, category in zip(poi['points_id'], poi['category'])]
        data = {
            'ids': poi['points_id'],
            'category': poi['category'],
            'locations': [graph.nodes[nd]['location'] for nd in poi['points_id']],
            'nv': nv,
            'num_vehicles': 1,
            'depot': nv - 1,
            'constraints': poi['constraints'],
            'distance_matrix': distance_matrix,
            'rewards': reward,
            'stop_time': stop_time,
            'info': [points_info[nd] for nd in poi['points_id']]
        }
        return OsmGraph(graph, way, data)

    def save(self, file_name):
        """
        Сохраняет OsmGraph в cash.

        Args:
            file_name - путь по которому необходимо сохранить файл.
        """
        with open(file_name, 'wb') as f:
            pickle.dump((self.graph, self.way, self.data), f)

    @staticmethod
    def load(file_name):
        """
        Загрузка OsmGraph из cash.

        Args:
            file_name - путь по которому сохренен файл.
        """
        with open(file_name, 'rb') as f:
            graph, way, data = pickle.load(f)
            return OsmGraph(graph, way, data)

    def _poi_location(self, point):
        """
        Создание словаря свойств poi.

        Args:
            point(int) - индекс(в ids) poi.

        Returns:
            dict - словарь c локацией poi и категорией.
                lng(float) - долгота.
                lat(float) - широта.
                category(str) - категория poi.
        """
        params = {'lng': self.data['locations'][point][1],
                  'lat': self.data['locations'][point][0],
                  'category': self.data['category'][point],
                  'attributes': self.data['attributes'][point]}
        return params
