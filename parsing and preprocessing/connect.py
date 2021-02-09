from pymongo import MongoClient
import os

client = MongoClient('localhost', 27017)
db = client['database']

cdir = os.environ.get('OSM_GRAPH_CACHE_DIR', os.path.dirname(__file__) + '/cache')
cdir1 = 'all'