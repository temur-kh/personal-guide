from Parse_data.attractions import parse_attractions
from Parse_data.food import parse_food

PATH = "./data/"

cities = {
    'Kaliningrad': {
        'id': 298500,
        'query': 800,
        'lon_min': 20.2135,
        'lon_max': 20.7614,
        'lat_min': 54.5847,
        'lat_max': 54.8066},
    'SaintPetersburg': {
        'id': 298507,
        'query': 10000,
        'lon_min': 29.8553,
        'lon_max': 30.8537,
        'lat_min': 59.7238,
        'lat_max': 60.1647},
    'Berlin': {
        'id': 187323,
        'query': 8000,
        'lon_min': 37.9509,
        'lon_max': 38.1301,
        'lat_min': 44.5364,
        'lat_max': 44.6309}}

def parse():
    parse_food(PATH + 'food/', cities)
    parse_attractions(PATH + 'attractions/', cities)
