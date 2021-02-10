import json
import os


def read_food(filename):
    files = os.listdir(path=filename)
    nodes = {}
    for file in files:
        with open(filename + file, 'r', encoding='utf-8') as f:
            text = json.load(f)
        for data in text['results']['data']:
            nodes[data['location_id']] = {'id': data['location_id'],
                                          'name': data.get('name'),
                                          'lat': data.get('latitude'),
                                          'lon': data.get('longitude'),
                                          'cuisine': data.get('cuisine'),
                                          'dietary_restrictions': data.get('dietary_restrictions'),
                                          'hours': data.get('hours'),
                                          'photo': data.get('photo'),
                                          'awards': data.get('awards'),
                                          'rating': data.get('rating'),
                                          'raw_ranking': data.get('raw_ranking'),
                                          'ranking_position': data.get('ranking_position'),
                                          'num_reviews': data.get('num_reviews'),
                                          'ranking_category': data.get('ranking_category'),
                                          'price_level': data.get('price_level'),
                                          'price': data.get('price')}
    return nodes
