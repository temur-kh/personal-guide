def get_element(element, city):
    info = {'location': element.element.location,
            'id_osm': element.id,
            'road': element.road,
            'important': element.important,
            'city': city}
    if element.entrance is not None:
        info['entrance'] = element.entrance

    if element.type == 'node':
        info['save'] = element.element.save
        info['crossroads'] = element.element.road['crossroads']
        if element.name is not None:
            info['name'] = element.name
        if element.old_name is not None:
            info['old_name'] = element.old_name
        if len(element.tags) > 0:
            info['tags'] = element.tags
            info['global_tags'] = element.global_tags


    if element.type == 'way':
        info['nodes'] = element.element.nodes
        info['simple_way'] = element.element.simple_nodes
        info['simple_nodes'] = element.element.simple_way
        info['length'] = element.element.length
        if element.road:
            info['tags'] = element.tags
            info['global_tags'] = element.global_tags

    if element.type == 'relation':
        info['ways'] = element.element.ways

    if element.place.get('id_place') is not None:
        info['id_place'] = element.place['id_place']
        info['rate'] = int(element.place['rate']) - 3 if int(element.place['rate']) > 3 else int(element.place['rate'])
        info['kinds'] = element.place['kinds']
    if element.place.get('description') is not None:
        info['description'] = element.place['description']

    if element.food.get('id') is not None:
        info['id_food'] = element.food['id']
        info['name_food'] = element.food['name']
        food_tags = ['cuisine', 'dietary_restrictions', 'hours', 'photo', 'awards', 'rating', 'raw_ranking',
                     'ranking_position', 'num_reviews', 'ranking_category', 'price_level', 'price']
        for tag in food_tags:
            if element.food[tag] is not None:
                info[tag] = element.food[tag]
    return info


def add_to_db(db, nodes, ways, relations, city):
    nodes_list = [get_element(node, city) for _, node in nodes.items()]
    db.nodes.insert_many(nodes_list)

    ways_list = [get_element(way, city) for _, way in ways.items()]
    db.ways.insert_many(ways_list)

    relations_list = [get_element(rel, city) for _, rel in relations.items()]
    db.relations.insert_many(relations_list)
