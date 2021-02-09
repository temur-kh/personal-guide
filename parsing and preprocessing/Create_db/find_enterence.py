import numpy as np
from shapely.geometry import Polygon, Point, LinearRing, LineString
from shapely.ops import nearest_points
from pymongo import MongoClient

from Class.Element import Element


def new_element(poly_coord, id_new):
    if len(poly_coord) > 2:
        poly = Polygon(poly_coord)
        lat = poly.centroid.coords[0][0]
        lon = poly.centroid.coords[0][1]
    else:
        lat = np.mean([poly_coord[i][0] for i in range(len(poly_coord))])
        lon = np.mean([poly_coord[i][1] for i in range(len(poly_coord))])
    new_elem = Element(id_new, 'node')
    new_elem.element.location['coordinates'] = [lon, lat]
    new_elem.entrance = True

    return new_elem


def find_point(way, point, id_new):
    way_coord = [[r[x] for x in [1, 0]] for r in way.element.location['coordinates']]
    point_coord = [point.element.location['coordinates'][x] for x in [1, 0]]
    p = nearest_points(LineString(way_coord), Point(point_coord))[0]
    if p == Point(point_coord):
        p = nearest_points(LineString(way_coord), Point(point_coord))[1]

    new_elem = Element(id_new, 'node')
    new_elem.element.location['coordinates'] = [p.y, p.x]
    new_elem.element.road['crossroads'] = True
    new_elem.road = True
    new_elem.element.road['start_end'] = True

    # НАЙТИ ТОЧКУ В ЛИНИИ
    min_dist = 1e9
    min_i = 0
    for i in range(len(way_coord) - 1):
        line = LineString([way_coord[i], way_coord[i + 1]])
        dist = p.distance(line)
        if dist < min_dist:
            min_dist = dist
            min_i = i
        # if line.within(p):
        #     way.element.location['coordinates'] = way.element.location['coordinates'][:i + 1] + \
        #                                           [new_elem.element.location['coordinates']] + \
        #                                           way.element.location['coordinates'][i + 1:]
        #     way.element.nodes = way.element.nodes[:i + 1] + [id_new] + way.element.nodes[i + 1:]
        #     break
    way.element.location['coordinates'] = way.element.location['coordinates'][:min_i + 1] + \
                                          [new_elem.element.location['coordinates']] + \
                                          way.element.location['coordinates'][min_i + 1:]
    way.element.nodes = way.element.nodes[:min_i + 1] + [id_new] + way.element.nodes[min_i + 1:]

    return way, new_elem, [point.id, id_new], [point.element.location['coordinates'],
                                               new_elem.element.location['coordinates']]


def find_enterence(nodes, ways, relations):
    cnt = 0
    for id_way, way in ways.items():
        if way.important and way.entrance is None:
            for id_node in way.element.nodes:
                if nodes[id_node].road and way.entrance is None:
                    way.entrance = id_node
                    nodes[id_node].entrance = True

    for id_rel, rel in relations.items():
        if rel.important and rel.entrance is None:
            for id_way in rel.element.ways:
                for id_node in ways[id_way].element.nodes:
                    if nodes[id_node].road and rel.entrance is None:
                        rel.entrance = id_node
                        nodes[id_node].entrance = True

    for id_way, way in ways.items():
        if way.important and way.entrance is None:
            poly_coord = [[r[x] for x in [1, 0]] for r in way.element.location['coordinates']]
            id_new = 'add_' + str(cnt)
            cnt += 1
            new_elem = new_element(poly_coord, id_new)
            nodes[id_new] = new_elem
            way.entrance = id_new

    for id_rel, rel in relations.items():
        if rel.important and rel.entrance is None:
            poly_coord = [[nodes[j].element.location['coordinates'][x] for x in [1, 0]]
                          for i in rel.element.outer for j in ways[i].element.nodes]
            id_new = 'add_' + str(cnt)
            cnt += 1
            new_elem = new_element(poly_coord, id_new)
            nodes[id_new] = new_elem
            rel.entrance = id_new

    for id_way, way in ways.items():
        if way.important and way.entrance is not None:
            nodes[way.entrance].important = way.important
            nodes[way.entrance].name = way.name
            nodes[way.entrance].old_name = way.old_name
            nodes[way.entrance].tags = way.tags
            nodes[way.entrance].global_tags = way.global_tags
            nodes[way.entrance].entrance = id_way

    for id_rel, rel in relations.items():
        if rel.important and rel.entrance is not None:
            nodes[rel.entrance].important = rel.important
            nodes[rel.entrance].name = rel.name
            nodes[rel.entrance].old_name = rel.old_name
            nodes[rel.entrance].tags = rel.tags
            nodes[rel.entrance].global_tags = rel.global_tags
            nodes[rel.entrance].entrance = id_rel

    client = MongoClient('localhost', 27017)
    db = client['database_1']

    new_nodes = {}
    del_nodes = {}
    for id_node, node in nodes.items():
        if not node.road and node.important:
            near_way = list(db.ways.find({'road': True,
                                          'location': {'$near': {
                                              '$geometry': {
                                                  'type': 'LineString',
                                                  'coordinates': node.element.location['coordinates']},
                                              '$maxDistance': 100}}}).limit(2))
            if len(near_way) == 0:
                print(node.element.location['coordinates'])
            else:
                if node.element.location['coordinates'] in ways[near_way[0]['id_osm']].element.location['coordinates']:
                    index = ways[near_way[0]['id_osm']].element.location['coordinates'].index(node.element.location['coordinates'])
                    del_nodes[ways[near_way[0]['id_osm']].element.nodes[index]] = id_node
                    ways[near_way[0]['id_osm']].element.nodes[index] = id_node

                else:
                    id_new = 'add_' + str(cnt)
                    cnt += 1
                    new_way = Element(id_new, 'way')
                    new_way.road = True
                    ways[id_new] = new_way
                    id_node = 'add_' + str(cnt)
                    cnt += 1
                    ways[near_way[0]['id_osm']], new_nodes[id_node], ways[id_new].element.nodes, \
                    ways[id_new].element.location['coordinates'] = find_point(ways[near_way[0]['id_osm']], node,
                                                                              id_node)
                    node.element.road['start_end'] = True

                node.road = True
    for id_way, way in ways.items():
        for i in list(del_nodes.keys()):
            if i in way.element.nodes:
                way.element.nodes[way.element.nodes.index(i)] = del_nodes[i]

    for id_node, node in new_nodes.items():
        nodes[id_node] = node
    return nodes, ways, relations
