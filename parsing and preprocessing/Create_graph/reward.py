import os
import pickle
import numpy as np
from collections import defaultdict
import networkx as nx

from connect import cdir, db

tags = ['finance', 'food', 'pharmacy', 'post', 'shop', 'telephone', 'wc',
        'entertainment', 'religion', 'tourism', 'architecture', 'historic']
cities = ['Kaliningrad', 'SaintPetersburg', 'Berlin']


def reward():
    for city in cities:
        print('\n', city)
        fnam = os.path.join(cdir, city + '.pkl')
        with open(fnam, 'rb') as f:
            graph, path = pickle.load(f)
        reward = defaultdict(lambda: {})
        for tag in tags:
            poi = list(db.poi.find({'city': city, 'global_tags': {'$in': [tag]}}))
            rewards = np.array([p['rate'] if p.get('rate') is not None
                                else (float(p['raw_ranking']) * 3 / 5 if p.get('raw_ranking') is not None
                                      else np.nan) for p in poi])

            centralities = np.array([graph.nodes[p['id_osm']]['centrality'][tag] for p in poi])
            rewards = np.array([centralities[i] if np.isnan(rewards[i]) else max(rewards[i], centralities[i])
                                for i in range(len(poi))])

            rewards = (10 * rewards).astype(int)
            for i in range(len(poi)):
                reward[poi[i]['id_osm']][tag] = max(1, rewards[i])

        reward = dict(reward)
        nx.set_node_attributes(graph, reward, 'reward')
        with open(fnam, 'wb') as f:
            pickle.dump((graph, path), f)