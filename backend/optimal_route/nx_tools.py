import networkx as nx
import numpy as np
from my_osm_graph import MyOsmGraph


def create_graph(lat, lon, dist=10000):
    return MyOsmGraph(lat, lon, dist=dist)


def find_nodes_in_graph(og, data):
    ids = data.get('ids')
    if ids is not None:
        return ids
    nv = data['nv']
    ids = []
    for iv in range(nv):
        pid = og.find_node(data['lats'][iv], data['lons'][iv])
        ids.append(pid)
    data['ids'] = ids
    return ids


def find_node_in_graph(og, point):
    pid = og.find_node(point[0], point[1])
    return pid


def nx_dijkstra_path(G, a, b):
    length, path = nx.single_source_dijkstra(G, a, b)
    return length, path


class RoutingPath:
    """
    Path from node (id) to another node on the map
    """

    def __init__(self, a, b, graph=None):
        self.start = a
        self.end = b
        self.use_nx = True
        if graph is None:
            self.path = []
            self.length = 0
        else:
            self.calculate_path_on_graph(graph)

    def calculate_path_on_graph(self, graph):
        if self.use_nx:
            self.length, self.path = nx_dijkstra_path(graph, self.start, self.end)
        else:
            print('Not implemented yet')

    def get_distance(self):
        return self.length

    def get_path(self):
        return self.path

    def info(self):
        print(f'Route from {self.start} to {self.end} len = {self.length}')


def dijkstra_all_paths_for_list(graph, nodes):
    paths = {}
    print('Calculating dijkstra_all_paths_for_list')
    for a in nodes:
        paths[a] = {}
        for b in nodes:
            if a == b:
                continue
            paths[a][b] = RoutingPath(a, b, graph)

    return paths


def dijkstra_paths_for_point(graph, paths, nodes, pid, need_return):
    # check if pid already in paths
    for a in nodes:
        if a == pid:
            return 0

    paths[pid] = {}
    for a in nodes:
        paths[pid][a] = RoutingPath(pid, a, graph)
        if need_return:
            paths[a][pid] = RoutingPath(a, pid, graph)  # if routes are symmetrical --> can inv?
        else:
            paths[a][pid] = RoutingPath(a, pid, None)

    return 1
