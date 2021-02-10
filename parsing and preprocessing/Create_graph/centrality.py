import os
import pickle
from collections import defaultdict
import networkx as nx

from connect import cdir, db

tags = ['finance', 'food', 'pharmacy', 'post', 'shop', 'telephone', 'wc', 'entertainment', 'religion', 'tourism',
        'architecture', 'historic']
INF = 5_000_000


def centrality():
    cities = ['Kaliningrad', 'SaintPetersburg', 'Berlin']
    for city in cities:

        print(city)
        fcity = os.path.join(cdir, f'{city}_poi.pkl')
        with open(fcity, 'rb') as f:
            graph_poi, path = pickle.load(f)
        centrality = defaultdict(lambda: {})
        for tag in tags:
            min_centrality = 1.0
            max_centrality = 0.0
            poi = list(db.poi.find({'city': city, 'global_tags': {'$in': [tag]}}))
            poi = [nd['id_osm'] for nd in poi]
            for i in range(len(poi)):
                print("\r {} : {}/{}.".format(tag, i + 1, len(poi)), end="")
                point = poi[i]
                try:
                    length = nx.single_source_dijkstra_path_length(graph_poi, point)
                except nx.NetworkXNoPath:
                    length = {}
                current_centrality = (len(poi) - 1) / sum(length.get(nd) for nd in poi)
                min_centrality = min(min_centrality, current_centrality)
                max_centrality = max(max_centrality, current_centrality)
                centrality[point][tag] = current_centrality
            print(min_centrality, max_centrality)
            for k, v in centrality.items():
                if v.get(tag) is not None:
                    centrality[k][tag] = 3.0 * (centrality[k][tag] - min_centrality) / \
                                             (max_centrality - min_centrality)
        centrality = dict(centrality)
        nx.set_node_attributes(graph_poi, centrality, 'centrality')
        with open(fcity, 'wb') as f:
            pickle.dump((graph_poi, path), f)