import pickle
from graph_constructor.graph import Graph


class OsmGraph(Graph):
    def __init__(self, graph, way, data):
        super().__init__()
        self.graph = graph
        self.way = way
        self.data = data

    def get_way(self, path):
        if len(self.data['ids']) > 0:
            line_string = []
            for iv, jv in zip(path[:-1], path[1:]):
                poi_path = self.data['poi_path'][iv][jv]
                for i, j in zip(poi_path[:-1], poi_path[1:]):
                    for line in self.way[i][j]:
                        line_string.append(line)
            return line_string
        return []

    def save(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump((self.graph, self.way, self.data), f)

    @staticmethod
    def load(file_name):
        with open(file_name, 'rb') as f:
            graph, way, data = pickle.load(f)
            return OsmGraph(graph, way, data)
