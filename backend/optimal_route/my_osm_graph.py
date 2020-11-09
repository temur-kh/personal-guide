import os, pickle, overpy, networkx as nx, matplotlib.pyplot as plt
from math import cos, pi, sqrt
from functools import lru_cache


class MyOsmGraph:
    earth_rad = 6371  # radius of earth(km)
    len1deg = earth_rad / 180 * pi * 1000  # m/度

    def __init__(self, lat, lon, dist=100, cache=True,
                 blst=()):
        self.coe = cos(lat / 180 * pi)
        self.key = f'{lat}_{lon}_{dist}'
        dy = dist / MyOsmGraph.len1deg
        dx = dy / self.coe
        ymin, xmin, ymax, xmax = lat - dy, lon - dx, lat + dy, lon + dx
        self.range = ymin, xmin, ymax, xmax
        cdir = os.environ.get('OSM_GRAPH_CACHE_DIR',
            os.path.dirname(__file__) + '/cache')
        if not os.path.isdir(cdir):
            os.mkdir(cdir)
        fnam = os.path.join(cdir, f'osm_graph_{self.key}.pkl')
        if cache and os.path.isfile(fnam):
            with open(fnam, 'rb') as fp:
                self.graph, self.pos = pickle.load(fp)
            return
        api = overpy.Overpass()
        result = api.query(f"""
            way({ymin},{xmin},{ymax},{xmax})["highway"];
            (._;>;);
            out body;""")
        blst = set(blst)
        self.graph = nx.Graph()
        inbox, self.pos = set(), {}
        for way in result.ways:
            if way.tags.get('highway') in blst:
                continue
            for nd in way.nodes:
                if ymin <= nd.lat <= ymax and xmin <= nd.lon <= xmax:
                    inbox.add(nd.id)
                if nd.id not in self.pos:
                    self.pos[nd.id] = float(nd.lon), float(nd.lat)
                    self.graph.add_node(nd.id, lat=float(nd.lat),
                        lon=float(nd.lon), **nd.tags)
            for nd1, nd2 in zip(way.nodes[:-1], way.nodes[1:]):
                if nd1.id in inbox or nd2.id in inbox:
                    dis = self.distance(nd1.id, nd2.id)
                    self.graph.add_edge(nd1.id, nd2.id, weight=dis, **way.tags)
        with open(fnam, 'wb') as fp:
            pickle.dump((self.graph, self.pos), fp)

    @lru_cache(maxsize=4096)
    def distance(self, nd1, nd2):
        x1, y1 = self.pos[nd1]
        x2, y2 = self.pos[nd2]
        return sqrt(((x1 - x2) * self.coe)**2 + (y1 - y2)**2) * MyOsmGraph.len1deg

    def find_node(self, lat, lon):
        c = cos(lat / 180 * pi)
        r, dis = None, 1e308
        for k, v in self.pos.items():
            d = abs(lat - v[1]) + abs(lon - v[0]) * c
            if d < dis:
                r, dis = k, d
        return r

    def draw_graph(self, figsize=(4, 4), graph=None, ax=None, **kwargs):
        if ax is None:
            ax = plt.figure(figsize=figsize).add_subplot(111)
        plt.ylim(self.range[0:3:2])
        plt.xlim(self.range[1:4:2])
        nx.draw_networkx(graph or self.graph, pos=self.pos,
            ax=ax, node_size=2, with_labels=False, **kwargs)
        return ax

    def __str__(self):
        return self.key
