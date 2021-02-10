import json
import os
import pickle
import multiprocessing as mp
import networkx as nx

from connect import cdir1, db, cdir

MAX_DISTANCE = 2_000


def mpCalcDistance_Worker(nodes, queue, graph, poi):
    # client = MongoClient('localhost', 27017)
    # db = client['database']
    while True:
        job = queue.get()
        if job == None:
            break
        print("\rCheck {}.".format(job + 1), end="")
        result = {}
        try:
            length, path = nx.single_source_dijkstra(graph, nodes[job]['id_osm'], cutoff=MAX_DISTANCE)
            result = {k: int(length[k]) for k in poi if k in length.keys()}
        except nx.NetworkXNoPath:
            pass
        id_osm = nodes[job]['id_osm']
        fnam = os.path.join(cdir1, f'{id_osm}.pkl')
        with open(fnam, 'w') as fp:
            json.dump(result, fp)
        id_ = nodes[job]['_id']
        db.nodes_graph.update({'_id': id_}, {'$set': {'dist_matrix': result}})
        queue.task_done()
    queue.task_done()


def mpCalcDistance(nodes, graph, poi):
    nCPU = 8
    n = len(nodes)
    start = 0
    end = 30000
    while start < n:
        queue = mp.JoinableQueue()
        for i in range(start, min(n, end)):
            queue.put(i)
            print("\rCheck {}/{}.".format(i + 1, n), end="")

        for i in range(nCPU):
            queue.put(None)
        workers = []
        for i in range(nCPU):
            worker = mp.Process(target=mpCalcDistance_Worker,
                                args=(nodes, queue, graph, poi,))
            workers.append(worker)
            worker.start()
        queue.join()
        start = end
        end += 30000
        print()


def distance():
    cities = ['Berlin']
    for city in cities:
        print(city)
        fcity = os.path.join(cdir, city + '.pkl')
        with open(fcity, 'rb') as f:
            _, graph, _ = pickle.load(f)
        nodes = list(db.nodes_graph.find({'city': city}))
        poi = list(db.poi.find({'city': city}))
        poi = [point['id_osm'] for point in poi]
        print(len(nodes))
        mpCalcDistance(nodes, graph, poi)
