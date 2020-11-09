# -*- coding: utf-8 -*-

from OSMPythonTools.nominatim import Nominatim
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import math

MAX_NODES = 10

start_coords = [52.5198810, 13.4073380]

map_distance = 0.01

def set_start_coords(x, y):
    global start_coords
    start_coords[0] = x
    start_coords[1] = y

def set_map_distance(d):
    global map_distance
    map_distance = d * 0.01

def coords_to_int(data):
    scaling = 10000000
    return int(data * scaling) % 10000000


dimensions = OrderedDict([
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
    })),
])

overpass = Overpass()
data_nodes = {}


def fetch(city):
    nominatim = Nominatim()
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"amenity"="cafe"', out='body')
    num_cafe = overpass.query(query, timeout=60).countElements()
    print('city {} has {} cafe'.format(city, num_cafe))
    nodes = overpass.query(query, timeout=60).elements()
    cafes = []
    lons = []
    lats = []
    n_nodes = 0
    for n in nodes:
        dist_to_center = math.hypot(n.lat() - start_coords[0], n.lon() - start_coords[1])
        if dist_to_center > map_distance:
            continue
        lons.append(n.lon())
        lats.append(n.lat())
        x, y = coords_to_int(n.lat()), coords_to_int(n.lon())
        cafes.append((x, y))
        n_nodes += 1
        if n_nodes >= MAX_NODES:
            break

    print('Consider only {} cafes'.format(len(cafes)))
    data_nodes['locations'] = cafes  # unused ?
    data_nodes['num_vehicles'] = 1
    data_nodes['depot'] = 0
    data_nodes['lons'] = lons
    data_nodes['lats'] = lats
    data_nodes['nv'] = n_nodes
    return overpass.query(query, timeout=60)


def get_berlin_cafes():
    data = Data(fetch, dimensions)
    return data_nodes
