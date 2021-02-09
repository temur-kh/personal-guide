import os

import requests
import json

MAX_ELEMENT = 500
KEY = ""

headers = {
    'x-rapidapi-host': "opentripmap-places-v1.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


def read_box(lon_min, lon_max, lat_min, lat_max, full_path, index, url):
    querystring = {"lon_min": str(lon_min),
                   "lon_max": str(lon_max),
                   "lat_min": str(lat_min),
                   "lat_max": str(lat_max)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    if len(data['features']) < MAX_ELEMENT:
        with open(full_path + '_' + str(index) + '.json', 'w') as outfile:
            json.dump(data, outfile)
    else:
        lon_med = round(lon_min + (lon_max - lon_min) / 2, 4)
        lat_med = round(lat_min + (lat_max - lat_min) / 2, 4)

        read_box(lon_min, lon_med, lat_min, lat_med, full_path, index * 4 + 1, url)
        read_box(lon_min, lon_med, lat_med, lat_max, full_path, index * 4 + 2, url)
        read_box(lon_med, lon_max, lat_med, lat_max, full_path, index * 4 + 3, url)
        read_box(lon_med, lon_max, lat_min, lat_med, full_path, index * 4 + 4, url)


def parse_attractions_by_features(path, cities):
    url = "https://opentripmap-places-v1.p.rapidapi.com/en/places/bbox"
    for name in cities.keys():
        read_box(cities[name]['lon_min'],
                 cities[name]['lon_max'],
                 cities[name]['lat_min'],
                 cities[name]['lat_max'],
                 path + name + '/features/' + name, 0, url)


def parse_attractions_by_id(path, cities):
    url = "https://opentripmap-places-v1.p.rapidapi.com/en/places/xid/"

    for name in cities:
        full_path = path + name + '/features/'
        files = os.listdir(path=full_path)
        for file in files:
            with open(full_path + file, 'r') as read_file:
                data = json.load(read_file)
            for info in data['features']:
                response = requests.request("GET", (url + info['id']), headers=headers)
                with open(path + name + '/by_id/' + info['id'] + '.json', 'w') as outfile:
                    json.dump(response.json(), outfile)


def parse_attractions(path, cities):
    parse_attractions_by_features(path, cities)
    parse_attractions_by_id(path, cities)
