import route_tools as rt

import nx_tools as nxt
import data as dt
import osmp_tools as ost
import time

MAX_DISTANCE_IN_MAP = 10000


class Optimizer:
    def __init__(self, speed=100, graph=None):
        self.og = graph
        self.speed = speed  # in m / min
        return

    def estimate_graph_distance_from_walking_dist(self, d):
        """
        in:
              d - расстояние в метрах, которое пройдет пользователь
        out:
            расстояние в метрах, по которому строится граф (квадрат 2n x 2n)
        """
        map_d_in_m = d / 2
        if map_d_in_m > MAX_DISTANCE_IN_MAP:
            map_d_in_m = MAX_DISTANCE_IN_MAP
        return map_d_in_m

    def estimate_walking_distance_from_time(self, t):
        """
            Having time in minutes, estimate distance in m
        """

        return self.speed * t

    def solve(self, starting_point, points_of_interest, time_for_route, need_return=False,
              paths=None):
        """
            starting_point - стартовая точка (координаты)
            points_of_interest - словарь с интересующими точками
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)
        graph_dist = self.estimate_graph_distance_from_walking_dist(walking_dist)
        print(f'graph_dist = {graph_dist}')
        if self.og is None:
            print('create_graph ...')
            self.og = nxt.create_graph(starting_point[0], starting_point[1], graph_dist)

        print('find_nodes_in_graph')
        poi_ids = nxt.find_nodes_in_graph(self.og, points_of_interest)
        starting_point_id = nxt.find_node_in_graph(self.og, starting_point)

        if paths is None:
            start = time.time()
            poi_paths = nxt.dijkstra_all_paths_for_list(self.og.graph, poi_ids)
            end = time.time()
            print('Points of interest: dijkstra time {}'.format(end - start))
        else:
            poi_paths = paths

        if starting_point_id not in poi_ids:
            start = time.time()
            nxt.dijkstra_paths_for_point(self.og.graph, poi_paths, poi_ids, starting_point_id, need_return)
            end = time.time()
            print('Dijkstra time for Starting point: {}'.format(end - start))
            dt.add_new_starting_point(points_of_interest, starting_point, starting_point_id)

        print('fill_distance_matrix')
        distances = rt.fill_distance_matrix(points_of_interest, poi_paths)

        start = time.time()
        route = rt.test_ortools(points_of_interest, distances=True, hard=True)
        end = time.time()
        print('OR calculation time is {}'.format(end - start))

        return route, poi_paths
