from fuzzywuzzy import fuzz
from haversine import haversine, Unit
import numpy as np

DIST = 600


def lat_lon(type, coord):
    if type == 'Point':
        lat = coord[1]
        lon = coord[0]
    if type == 'LineString':
        lat = np.mean([coord[i][1] for i in range(len(coord))])
        lon = np.mean([coord[i][0] for i in range(len(coord))])
    return (lat, lon)


def find_elements(connection, collection, type, node, elem_type):
    elements = list(collection.find({'name': {'$exists': True},
                                     'global_tags': {'$all': ['food']},
                                     'location': {'$near': {
                                         '$geometry': {
                                             'type': type,
                                             'coordinates': [float(node['lon']), float(node['lat'])]},
                                         '$maxDistance': DIST}}}))
    for elem in elements:
        id = elem['id_osm']
        name = elem['name']
        old_name = elem.get('old_name')
        dist = haversine((float(node['lon']), float(node['lat'])),
                         lat_lon(type, elem['location']['coordinates']), Unit.METERS)
        info = {'name_food': node['name'],
                'id': id,
                'name': name,
                'tags': elem.get('tags'),
                'Lihtenshtein': 100,
                'dist': dist,
                'type': elem_type}
        if node['name'] == name or node['name'] == old_name:
            if connection.get(node['id']) == None:
                connection[node['id']] = info
            elif connection.get(node['id'])['dist'] > dist:
                connection[node['id']] = info
        else:
            size = fuzz.ratio(node['name'], name)
            if old_name != None:
                size = min(size, fuzz.ratio(node['name'], old_name))
            if size > 50:
                info['Lihtenshtein'] = size
                if connection.get(node['id']) == None:
                    connection[node['id']] = info
                elif connection.get(node['id'])['Lihtenshtein'] < size:
                    connection[node['id']] =info
                elif connection.get(node['id'])['dist'] > dist:
                    connection[node['id']] = info
    return connection


def find_food(db, nodes_food, nodes, ways, relations):
    connection = {}
    for id_food in nodes_food.keys():
        lat_food = nodes_food[id_food]['lat']
        lon_food = nodes_food[id_food]['lon']
        if lat_food != None and lon_food != None:
            connection = find_elements(connection, db.nodes, 'Point', nodes_food[id_food],'node')
            # connection = find_elements(connection, db.ways, 'LineString', nodes_food[id_food], 'way')
            # connection = find_elements(connection, db.relations, 'MultiLineString', nodes_food[id_food], 'relation')
    for food_id, data in connection.items():
        if data['type'] == 'node':
            nodes[data['id']].food = nodes_food[food_id]
        # if data['type'] == 'way':
        #     ways[data['id']].food = nodes_food[food_id]
        # if data['type'] == 'relation':
        #     relations[data['id']].food = nodes_food[food_id]
    return nodes, ways, relations
