from Create_db.find_enterence import find_enterence
from pymongo import MongoClient


def clear_dataset(nodes, ways, relations, city):
    del_ways = []
    for id_way, way in ways.items():
        if len([1 for id in way.element.nodes if nodes.get(id) == None]) > 0:
            del_ways.append(id_way)
        else:
            way.element.set_location([nodes[i].element.location['coordinates'] for i in way.element.nodes])
            for i in range(len(way.element.nodes)):
                position = 'input' if 0 < i < (len(way.element.nodes) - 1) else 'start_end'
                nodes[way.element.nodes[i]].element.road[position] += 1
                if way.road:
                    nodes[way.element.nodes[i]].road = way.road
                if nodes[way.element.nodes[i]].entrance is not None:
                    way.entrance = way.element.nodes[i]
    for i in del_ways:
        del ways[i]

    del_rel = []
    for id_rel, rel in relations.items():
        if len([1 for i in rel.element.ways if ways.get(i) is None]) > 0:
            del_rel.append(id_rel)
        else:
            if len(rel.element.ways) == 0:
                del_rel.append(id_rel)
            else:
                rel.element.set_location([ways[i].element.location['coordinates'] for i in rel.element.outer])
                for i in rel.element.ways:
                    if ways[i].entrance is not None:
                        rel.entrance = ways[i].entrance
    for i in del_rel:
        del relations[i]

    nodes, ways, relations = find_enterence(nodes, ways, relations)


    del_nodes = []
    for id_node, node in nodes.items():

        node.is_save()

        if node.element.road['start_end'] + node.element.road['input'] == 0 and \
                len(node.tags) == 0 and \
                node.entrance is None and \
                not node.road:
            del_nodes.append(id_node)
    for id_way, way in ways.items():
        way.element.simple_way = [i for i in way.element.nodes if nodes[i].element.save]
        way.element.len(nodes)
    for i in del_nodes:
        del nodes[i]

    return nodes, ways, relations
