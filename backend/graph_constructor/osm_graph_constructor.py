import os, pickle
from collections import defaultdict
import networkx as nx

from graph_constructor.osm_graph import OsmGraph
from graph_constructor.graph_constructor import GraphConstructor


class OsmGraphConstructor(GraphConstructor):

    def __init__(self, data_processor, cdir, cache=True):
        super().__init__()
        self.cdir = cdir
        self.cache = cache
        self.data_processor = data_processor
        if not os.path.isdir(cdir):
            os.mkdir(cdir)

    def create_graph(self, lat, lon, dist, tags, max_points=None):
        key = f'{lat}_{lon}_{dist}_{max_points}' + str(tags)
        fnam = os.path.join(self.cdir, f'osm_graph_{key}.pkl')
        if self.cache and os.path.isfile(fnam):
            with open(fnam, 'rb') as fp:
                graph, pos, path, points, data = pickle.load(fp)
                return OsmGraph(graph, pos, path, points['points'], data)
        else:
            graph = nx.Graph()
            pos = {}
            path = defaultdict(lambda: {})
            ways = self.find_way(lat, lon, dist)
            for way in ways:
                way_nd = way['simple_nodes']
                points = [coord[0] for coord in way['simple_way']] + [way['simple_way'][-1][-1]]
                pos.update({key: value for key, value in zip(way_nd, points)})
                graph.add_weighted_edges_from(zip(way_nd[:-1], way_nd[1:], way['length']), tags=way['global_tags'])
                for k, v, w in zip(way_nd[:-1], way_nd[1:], way['simple_way']):
                    path[k][v] = w
                    path[v][k] = list(reversed(w))
            path = dict(path)
            Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
            graph = graph.subgraph(Gcc[0]).copy()

            start_point = self.find_node(lat, lon, dist, graph)
            poi = self.find_poi(tags, lat, lon, dist, graph)
            if max_points is not None:
                poi = poi[:max_points]
            bg = OsmGraph(graph, pos, path, poi + [start_point])
            bg.save(fnam)
            return bg

    def find_way(self, lat, lon, dist):
        way = self.data_processor.select_query('ways', {'road': True,
                                                        'location': {'$near': {'$geometry': {'type': 'LineString',
                                                                                             'coordinates': [lon, lat]},
                                                                               '$maxDistance': dist}}})
        return way

    def find_node(self, lat, lon, dist, graph):
        nodes = self.data_processor.get_nearest_points(lat, lon, dist)
        nodes = [node['id_osm'] for node in nodes if node['id_osm'] in graph.nodes()]
        if len(nodes) > 0:
            return nodes[0]
        return None

    def find_poi(self, tags, lat, lon, dist, graph):
        nodes = self.data_processor.get_nearest_points(lat, lon, dist, tags)
        ids = [node['id_osm'] for node in nodes if node['id_osm'] in graph.nodes()]
        return ids
