from Create_db.add_to_db import add_to_db
from Create_db.clear_dataset import clear_dataset
from Create_db.find_food import find_food
from Create_db.read_attraction import read_attraction
from Create_db.read_food import read_food
from Create_db.read_osm import read_osm
from Tags.Tags import tags_filter
from connect import db

PATH = './data/'
cities = ['Kaliningrad',
          'SaintPetersburg',
          'Berlin']


def read():
    nodes = {}
    ways = {}
    relations = {}
    for city in cities:
        print('\n', city)
        nodes[city], ways[city], relations[city] = read_osm(PATH + 'osm/' + city + '.osm')
        nodes[city], ways[city], relations[city] = clear_dataset(nodes[city], ways[city], relations[city], city)
        nodes[city], ways[city], relations[city] = read_attraction(PATH + 'attractions/' + city + '/', nodes[city],
                                                                   ways[city], relations[city])
        nodes_food = read_food(PATH + 'food/' + city + '/RU/')
        nodes[city], ways[city], relations[city] = find_food(db, nodes_food, nodes[city], ways[city], relations[city])

    db.nodes.drop()
    db.ways.drop()
    db.relations.drop()

    db.nodes.create_index([('location', '2dsphere')])
    db.ways.create_index([('location', '2dsphere')])
    db.relations.create_index([('location', '2dsphere')])
    for city in cities:
        print('\n', city)
        add_to_db(db, nodes[city], ways[city], relations[city], city)

    db.poi.create_index([('location', '2dsphere')])
    db.poi.insert_many(list(db.nodes.find({'tags': {'$in': tags_filter}})))