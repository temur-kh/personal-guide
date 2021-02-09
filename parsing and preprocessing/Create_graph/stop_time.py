import os
import pickle
from collections import defaultdict
import numpy as np
import networkx as nx

from connect import cdir, db

INF = 5_000_000
times = {
    'entertainment': np.nan,
    'entertainment_art': 10,
    'entertainment_museum': 120,
    'entertainment_theatre': 120,
    'entertainment_cinema': 120,
    'entertainment_zoo': 120,
    'entertainment_park': 120,
    'entertainment_planetarium': 120,
    'entertainment_aquarium': 120,

    'religion': np.nan,
    'religion_building': 10,
    'religion_church': 20,

    'tourism': np.nan,
    'tourism_monument': 2,
    'tourism_sculpture': 2,
    'tourism_viewpoint': 20,
    'tourism_tourism': 5,
    'tourism_fountain': 2,

    'architecture': 2,

    'historic': np.nan,
    'historic_historic': 2,
    'historic_tomb': 2,
    'historic_military': 2,
    'historic_transport': 2,
    'historic_water': 2,
    'historic_city': 2,
    'historic_archaeological': 2,
    'historic_memorial': 2,

    'finance': np.nan,
    'finance_bank': 15,
    'finance_atm': 15,
    'finance_bureau_de_change': 15,

    'food': np.nan,
    'food_pub': 60,
    'food_fast': 30,
    'food_cafe': 60,
    'food_restaurant': 60,

    'pharmacy': 10,

    'post': np.nan,
    'post_box': 5,
    'post_office': 10,

    'shop': np.nan,
    'shop_bakery': 10,
    'shop_deli': 10,
    'shop_water': 10,

    'telephone': 20,

    'wc': 10
}

all_tags = {'finance': 'finance',
            'finance_bank': 'finance',
            'finance_atm': 'finance',
            'finance_bureau_de_change': 'finance',

            'food': 'food',
            'food_pub': 'food',
            'food_fast': 'food',
            'food_cafe': 'food',
            'food_restaurant': 'food',

            'pharmacy': 'pharmacy',

            'post': 'post',
            'post_box': 'post',
            'post_office': 'post',

            'shop': 'shop',
            'shop_bakery': 'shop',
            'shop_deli': 'shop',
            'shop_water': 'shop',
            'shop_supermarket': 'shop',

            'telephone': 'telephone',

            'wc': 'wc',

            'entertainment': 'entertainment',
            'entertainment_art': 'entertainment',
            'entertainment_museum': 'entertainment',
            'entertainment_theatre': 'entertainment',
            'entertainment_cinema': 'entertainment',
            'entertainment_zoo': 'entertainment',
            'entertainment_park': 'entertainment',
            'entertainment_planetarium': 'entertainment',
            'entertainment_aquarium': 'entertainment',

            'religion': 'religion',
            'religion_building': 'religion',
            'religion_church': 'religion',

            'tourism': 'tourism',
            'tourism_monument': 'tourism',
            'tourism_sculpture': 'tourism',
            'tourism_viewpoint': 'tourism',
            'tourism_tourism': 'tourism',
            'tourism_fountain': 'tourism',

            'architecture': 'architecture',

            'historic': 'historic',
            'historic_historic': 'historic',
            'historic_tomb': 'historic',
            'historic_military': 'historic',
            'historic_transport': 'historic',
            'historic_water': 'historic',
            'historic_city': 'historic',
            'historic_archaeological': 'historic',
            'historic_memorial': 'historic'
            }


def stop_time():
    min_time = 500
    cities = ['Kaliningrad', 'SaintPetersburg', 'Berlin']
    for city in cities:
        fcity = os.path.join(cdir, f'{city}_poi.pkl')
        with open(fcity, 'rb') as f:
            graph_poi, path = pickle.load(f)
        stop_time = defaultdict(lambda: {})
        poi = list(db.poi.find({'city': city}))
        for i in range(len(poi)):
            print("\r Check: {}/{}.".format(i + 1, len(poi)), end="")
            point = poi[i]
            global_tags = [all_tags[tag] for tag in point['global_tags']]
            for global_tag in set(global_tags):
                tags = [i for i, j in zip(point['global_tags'], global_tags) if j == global_tag]
                time_ = int(np.nanmean(np.array([times[tag] for tag in tags])))
                min_time = min(min_time, time_)
                stop_time[point['id_osm']][global_tag] = time_
        nx.set_node_attributes(graph_poi, stop_time, 'stop_time')
        with open(fcity, 'wb') as f:
            pickle.dump((graph_poi, path), f)
