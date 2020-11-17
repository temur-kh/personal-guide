import pickle

import networkx as nx

from graph_constructor.graph import Graph
import numpy as np


class OsmGraph(Graph):
    def __init__(self, graph, pos, way, points, data=None):
        super().__init__()
        self.graph = graph
        self.pos = pos
        self.way = way
        self.points = points
        self.data = data

    def get_distance(self):
        return self.data

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

    def create_data(self):
        nv = len(self.points)
        self.data = {'ids': self.points, 'locations': [self.pos[i] for i in self.points], 'nv': nv, 'num_vehicles': 1,
                     'depot': len(self.points) - 1, 'distance_matrix': np.zeros((nv, nv)), 'poi_path': {}}
        for iv in range(nv):
            i = self.points[iv]
            self.data['poi_path'][iv] = {}
            for jv in range(nv):
                j = self.points[jv]
                if iv != jv:
                    if self.data['poi_path'].get(jv) is not None:
                        self.data['distance_matrix'][iv][jv] = self.data['distance_matrix'][jv][iv]
                        self.data['poi_path'][iv][jv] = list(reversed(self.data['poi_path'][jv][iv]))
                    else:
                        length, path = nx.single_source_dijkstra(self.graph, i, j)
                        self.data['distance_matrix'][iv][jv] = length
                        self.data['poi_path'][iv][jv] = path

    def save(self, file_name):
        if self.data is None:
            self.create_data()
        with open(file_name, 'wb') as fp:
            pickle.dump((self.graph, self.pos, self.way, {'points': self.points}, self.data), fp)
