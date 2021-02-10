import os
import pickle
from collections import defaultdict
import networkx as nx

from connect import db, cdir

cities = ['Kaliningrad', 'SaintPetersburg', 'Berlin']


def simplify_graph():
    for city in cities:
        graph = nx.Graph()
        ways = list(db.ways.find({'road': True, 'city': city}))
        path = defaultdict(lambda: {})
        for way in ways:
            way_nd = way['simple_nodes']
            graph.add_weighted_edges_from(zip(way_nd[:-1], way_nd[1:], way['length']))
            for k, v, w in zip(way_nd[:-1], way_nd[1:], way['simple_way']):
                path[k][v] = w
                path[v][k] = list(reversed(w))
        for i, v in path.items():
            for j, p in v.items():
                path_cur = [p[0]]
                for nd1, nd2 in zip(p[:-1], p[1:]):
                    if nd1[0] != nd2[0] or nd1[1] != nd2[1]:
                        path_cur.append(nd2)
                path[i][j] = path_cur
        Gcc = sorted(nx.connected_components(graph), key=len, reverse=True)
        graph = graph.subgraph(Gcc[0]).copy()

        poi = list(db.poi.find({'city': city}))
        poi = [nd['id_osm'] for nd in poi]

        nodes = list(graph.nodes())
        n = len(nodes)
        for i in range(n):
            print("\rCheck {}/{}.".format(i + 1, n), end="")
            node = nodes[i]
            if graph.has_edge(node, node):
                graph.remove_edge(node, node)

        for i in range(n):
            print("\rCheck {}/{}.".format(i + 1, n), end="")
            node = nodes[i]
            if node not in poi:
                if graph.degree(node) < 4:
                    edges = list(graph.edges(node))
                    edges = [edge[1] for edge in edges]
                    if len(edges) > 1:
                        for j in range(len(edges)):
                            nd1 = edges[j]
                            nodes_for_split = edges[:j] + edges[j + 1:]
                            w1 = graph[nd1][node]["weight"]
                            w = [graph[nd2][node]["weight"] + w1 for nd2 in nodes_for_split]
                            for nd2, weight in zip(nodes_for_split, w):
                                if graph.has_edge(nd1, nd2):
                                    if graph[nd1][nd2]["weight"] > weight:
                                        graph[nd1][nd2]["weight"] = weight
                                        path[nd1][nd2] = path[nd1][node] + path[node][nd2][1:]
                                        path[nd2][nd1] = path[nd2][node] + path[node][nd1][1:]
                                else:
                                    graph.add_edge(nd1, nd2, weight=weight)
                                    path[nd1][nd2] = path[nd1][node] + path[node][nd2][1:]
                                    path[nd2][nd1] = path[nd2][node] + path[node][nd1][1:]
                    if len(edges) != 1:
                        graph.remove_node(node)

        split = []
        for i, j in list(graph.edges()):
            p = path[i][j]
            path_cur = [p[0]]
            for nd1, nd2 in zip(p[:-1], p[1:]):
                if nd1[0] != nd2[0] or nd1[1] != nd2[1]:
                    path_cur.append(nd2)
            if len(path_cur) == 1:
                split.append((i, j))

        while len(split) > 0:
            for nd1, nd2 in split:
                del_nd = nd1 if nd1 not in poi else nd2
                if graph.has_node(del_nd):
                    save_nd = nd2 if nd1 not in poi else nd1
                    edges = list(graph.edges(del_nd))
                    edges = [edge[1] for edge in edges if edge[1] != save_nd]
                    w = [graph[del_nd][nd]["weight"] for nd in edges]
                    for nd2, weight in zip(edges, w):
                        if graph.has_edge(save_nd, nd2):
                            if graph[save_nd][nd2]["weight"] > weight:
                                graph[save_nd][nd2]["weight"] = weight
                                path[save_nd][nd2] = path[save_nd][del_nd] + path[del_nd][nd2][1:]
                                path[nd2][save_nd] = path[nd2][del_nd] + path[del_nd][save_nd][1:]
                        else:
                            graph.add_edge(save_nd, nd2, weight=weight)
                            path[save_nd][nd2] = path[save_nd][del_nd] + path[del_nd][nd2][1:]
                            path[nd2][save_nd] = path[nd2][del_nd] + path[del_nd][save_nd][1:]
                    graph.remove_node(del_nd)
            split = []
            for i, j in list(graph.edges()):
                p = path[i][j]
                path_cur = [p[0]]
                for nd1, nd2 in zip(p[:-1], p[1:]):
                    if nd1[0] != nd2[0] or nd1[1] != nd2[1]:
                        path_cur.append(nd2)
                if len(path_cur) == 1:
                    split.append((i, j))

        new_path = defaultdict(lambda: {})
        for i, j in list(graph.edges()):
            p = path[i][j]
            path_cur = [p[0]]
            for nd1, nd2 in zip(p[:-1], p[1:]):
                if nd1[0] != nd2[0] or nd1[1] != nd2[1]:
                    path_cur.append(nd2)
            new_path[i][j] = path_cur
            new_path[j][i] = list(reversed(path_cur))

        print('\n', nx.number_of_nodes(graph), nx.number_of_edges(graph))
        fcity = os.path.join(cdir, f'{city}.pkl')
        with open(fcity, 'wb') as f:
            pickle.dump((graph, dict(new_path)), f)


def matrix():
    for city in cities:
        fcity = os.path.join(cdir, f'{city}.pkl')
        with open(fcity, 'rb') as f:
            graph, path = pickle.load(f)
        poi = list(db.poi.find({'city': city}))
        poi = [nd['id_osm'] for nd in poi]

        nodes = list(graph.nodes())
        nodes = [nd for nd in nodes if
                 nd not in poi and len([edge[1] for edge in list(graph.edges(nd)) if edge[1] != nd]) < 5]
        while len(nodes) > 0:
            n = len(nodes)
            for i in range(n):
                print("\rCheck {}/{}.".format(i + 1, n), end="")
                node = nodes[i]
                edges = list(graph.edges(node))
                edges = [edge[1] for edge in edges if edge[1] != node]
                if 1 < len(edges) < 5:
                    for j in range(len(edges)):
                        nd1 = edges[j]
                        nodes_for_split = edges[:j] + edges[j + 1:]
                        w1 = graph[nd1][node]["weight"]
                        w = [graph[nd2][node]["weight"] + w1 for nd2 in nodes_for_split]
                        for nd2, weight in zip(nodes_for_split, w):
                            if graph.has_edge(nd1, nd2):
                                if graph[nd1][nd2]["weight"] > weight:
                                    graph[nd1][nd2]["weight"] = weight
                                    path[nd1][nd2] = path[nd1][node] + path[node][nd2][1:]
                                    path[nd2][nd1] = path[nd2][node] + path[node][nd1][1:]
                            else:
                                graph.add_edge(nd1, nd2, weight=weight)
                                path[nd1][nd2] = path[nd1][node] + path[node][nd2][1:]
                                path[nd2][nd1] = path[nd2][node] + path[node][nd1][1:]
                    graph.remove_node(node)
                elif len(edges) < 2:
                    graph.remove_node(node)
            nodes = list(graph.nodes())
            nodes = [nd for nd in nodes if
                     nd not in poi and len([edge[1] for edge in list(graph.edges(nd)) if edge[1] != nd]) < 5]
        new_path = defaultdict(lambda: {})
        for i, j in list(graph.edges()):
            new_path[i][j] = path[i][j]
            new_path[j][i] = list(reversed(path[i][j]))

        fcity = os.path.join(cdir, f'{city}_poi.pkl')
        with open(fcity, 'wb') as f:
            pickle.dump((graph, dict(new_path)), f)
