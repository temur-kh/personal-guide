import os
from collections import defaultdict
import networkx as nx

from graph_constructor.osm_graph import OsmGraph
from graph_constructor.graph_constructor import GraphConstructor

MAX_DIST = 2_000
INF_DIST = 1_000_000


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
            return OsmGraph.load(fnam)
        else:
            graph = nx.Graph()
            path = defaultdict(lambda: {})
            ways = self.find_way(lat, lon, dist)
            for way in ways:
                way_nd = way['simple_nodes']
                graph.add_weighted_edges_from(zip(way_nd[:-1], way_nd[1:], way['length']), tags=way['global_tags'])
                for k, v, w in zip(way_nd[:-1], way_nd[1:], way['simple_way']):
                    path[k][v] = w
                    path[v][k] = list(reversed(w))
            path = dict(path)
            Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
            graph = graph.subgraph(Gcc[0]).copy()
            data = self.create_data(graph, lat, lon, dist, tags, max_points)
            osm_graph = OsmGraph(graph, path, data)
            osm_graph.save(fnam)
            return osm_graph

    def find_way(self, lat, lon, dist):
        way = self.data_processor.select_query('ways', {'road': True,
                                                        'location': {'$near': {'$geometry': {'type': 'LineString',
                                                                                             'coordinates': [lon, lat]},
                                                                               '$maxDistance': dist}}})
        return way

    def create_data(self, graph, lat, lon, dist, tags, max_points):
        points = self.find_poi(graph, lat, lon, dist, tags, max_points) + [self.find_node(graph, lat, lon)]
        data = {
            'ids': [i['id_osm'] for i in points],
            'locations': [[i['location']['coordinates'][x] for x in [1, 0]] for i in points],
            'nv': len(points),
            'num_vehicles': 1,
            'depot': len(points) - 1,
            'distance_matrix': [[]] * len(points),
            'poi_path': [[]] * len(points)
        }
        for i in range(data['nv']):
            start = data['ids'][i]
            try:
                length, path = nx.single_source_dijkstra(graph, start, cutoff=MAX_DIST)
                data['distance_matrix'][i] = [INF_DIST if length.get(nd) is None else length[nd] for nd in data['ids']]
                data['poi_path'][i] = [[] if path.get(nd) is None else path[nd] for nd in data['ids']]
            except nx.NetworkXNoPath:
                data['distance_matrix'][i] = [INF_DIST] * data['nv']
                data['poi_path'][i] = [[]] * data['nv']
                pass
        return data

    def find_node(self, graph, lat, lon):
        nodes = []
        dist = 100
        while len(nodes) == 0 and dist < 1_000:
            nodes = self.data_processor.get_nearest_points(lat, lon, dist)
            nodes = [node for node in nodes if node['id_osm'] in graph.nodes()]
            dist *= 2
        if len(nodes) > 0:
            return nodes[0]
        return None

    def find_poi(self, graph, lat, lon, dist, tags, max_points):
        nodes = self.data_processor.get_nearest_points(lat, lon, dist, tags)
        poi = [node for node in nodes if node['id_osm'] in graph.nodes()]
        if max_points is not None:
            poi = poi[:max_points]
        return poi
