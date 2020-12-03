import pickle
import networkx as nx

from graph_constructor.graph import Graph


class OsmGraph(Graph):
    def __init__(self, graph, way, data):
        """
        Params:
            graph(networkx.Graph) - граф города лтбо граф вокруг стратовой точки.
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
        if len(self.data['ids']) > 0:
            for iv, jv in zip(route[:-1], route[1:]):
                points.append(self._poi_location(iv))
                length, path = nx.single_source_dijkstra(self.graph, self.data['ids'][iv], self.data['ids'][jv])
                if length > 800:
                    print(self.data['ids'][iv], self.data['ids'][jv], length)
                for i, j in zip(path[:-1], path[1:]):
                    for line in self.way[i][j]:
                        line_string.append({'lng': line[1], 'lat': line[0]})
            points.append(self._poi_location(route[-1]))
        return points, line_string

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
                  'category': self.data['category'][point]}
        return params
