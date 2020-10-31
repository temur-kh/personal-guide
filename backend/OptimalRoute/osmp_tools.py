# -*- coding: utf-8 -*-

from OSMPythonTools.nominatim import Nominatim
from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

MAX_NODES = 200
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()


def coords_to_int(data):
    scaling = 10000000
    return int(data * scaling)

dimensions = OrderedDict([
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
    })),
])

overpass = Overpass()
data_nodes = {}
def fetch(city):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"amenity"="cafe"', out='body')
    num_cafe = overpass.query(query, timeout=60).countElements()
    print('city {} has {} cafe'.format(city, num_cafe))
    nodes = overpass.query(query, timeout=60).elements()
    cafes = []
    n_nodes = 0
    for n in nodes:
        #print ('({}, {})'.format(n.lat(), n.lon()))
        x, y = coords_to_int(n.lat()), coords_to_int(n.lon())
        cafes.append((x, y))
        n_nodes += 1
        if n_nodes >= MAX_NODES:
            break
        
    print('Consider only {} cafes'.format(len(cafes)))
    data_nodes['locations'] = cafes
    data_nodes['num_vehicles'] = 1
    data_nodes['depot'] = 0
    return overpass.query(query, timeout=60)

def get_berlin_cafes():
    data = Data(fetch, dimensions)
    return data_nodes
