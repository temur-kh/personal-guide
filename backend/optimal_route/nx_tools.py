import networkx as nx
import numpy as np
from osm_graph import OsmGraph

berlinCenter = (52.5198810, 13.4073380)


def create_graph(lat, lon, data):
    og = OsmGraph(lat, lon, dist=5000)
    nv = len(data['lats'])
    ids = np.zeros(nv, dtype=np.int64)
    for iv in range(nv):
        ivid = og.find_node(data['lats'][iv], data['lons'][iv])
        ids[iv] = ivid

    return og, ids


def dijkstra_path(G, a, b):
    path = nx.dijkstra_path(G, a, b)
    return path
