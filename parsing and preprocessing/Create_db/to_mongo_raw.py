from lxml import etree
import json
import os

from pymongo import MongoClient

PATH = './data/'
cities = ['Kaliningrad',
          'SaintPetersburg',
          'Berlin']

def to_mongo_raw():
    DATABASE = 'database'

    # client = MongoClient('mongodb://' + USERNAME + ':' + PASSWORD + '@' + IP + ':' + PORT + '/' + DATABASE)
    client = MongoClient('localhost', 27017)

    db = client[DATABASE]
    delete = False
    download = False
    result = False
    for city in cities:
        if delete:
            db.raw.delete_many({'city': city})
        if download:
            db.raw.insert_many(osm(PATH + 'osm/' + city + '.osm', city))
            # db.raw.insert_many(food(PATH + 'food/' + city + '/RU/', city))
        if result:
            res = list(db.raw.find({'city': city}))
            print(len(res))

def save_json():
    for city in cities:
        with open(city+'_osm.json', 'w') as f:
            json.dump(osm(PATH + 'osm/' + city + '.osm', city), f)
        with open(city+'_food.json', 'w') as f:
            json.dump(food(PATH + 'food/' + city + '/RU/', city), f)




def find_document(collection, elements, multiple=False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def osm(filename, city):
    elements = []
    tree = etree.iterparse(filename, events=('start', 'end',))
    type = ['node', 'way', 'relation']
    for event, elem in tree:
        if event == 'end' and elem.tag in type:
            element = {'id_osm': elem.get('id'),
                       'type': elem.tag,
                       'city': city}
            if elem.tag == 'node':
                element['location'] = {'coordinates': [elem.get('lon'), elem.get('lat')],
                                       'type': 'Point'}
            elif elem.tag == 'way':
                element['nodes'] = [child.get('ref') for child in elem.getchildren() if child.tag == 'nd']
            elif elem.tag == 'relation':
                element['ways'] = [child.get('ref') for child in elem.getchildren()
                                   if child.tag == 'member' and child.get('type') == 'way']
            for child in elem.getchildren():
                if child.tag == 'tag':
                    if element.get('tags') == None:
                        element['tags'] = {}
                    element['tags'][child.get('k').replace('.', '_')] = child.get('v')
            elements.append(element)
    print(len(elements))
    return elements


def food(filename, city):
    files = os.listdir(path=filename)
    foods = []
    for file in files:
        with open(filename + file, 'r', encoding='utf-8') as f:
            text = json.load(f)
        foods += text['results']['data']
    for data in foods:
        data['city'] = city
    print(len(foods))
    return foods
