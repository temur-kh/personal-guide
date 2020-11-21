from . import route_tools as rt
from . import nx_tools as nxt
from . import data as dt
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

    def solve(self, data, time_for_route, need_return=False):
        """
            starting_point - стартовая точка (координаты)
            points_of_interest - словарь с интересующими точками
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)
        graph_dist = self.estimate_graph_distance_from_walking_dist(walking_dist)
        print(f'graph_dist = {graph_dist}', flush=True)

        print('find_nodes_in_graph', flush=True)
        poi_paths = data['poi_path']

        print('fill_distance_matrix', flush=True)
        distance_matrix = data['distance_matrix']

        start = time.time()
        #  route = rt.test_ortools(points_of_interest, distances=True, hard=True)
        #  route = rt.find_ortools_route_with_distance_matrix(points_of_interest, distances, hard=True)
        route = rt.find_route_with_distance_limit(data, distance_matrix, walking_dist,
                                                  poi_paths, need_return, hard=True)
        end = time.time()
        print('OR calculation time is {}'.format(end - start), flush=True)

        return route, poi_paths
