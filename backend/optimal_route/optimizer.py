from . import route_tools as rt
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
            data - словарь с ключами:
                distance_matrix - матрица расстояний между всеми точками
                depot - индекс стартовой вершины
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)

        distance_matrix = data['distance_matrix']

        USE_OR_HEURISTIC = False

        start = time.time()
        if USE_OR_HEURISTIC:
            route = rt.find_route_with_distance_limit(data, distance_matrix, walking_dist,
                                                      need_return, hard=True)
        else:
            route = rt.reward_collecting_tsp(data, distance_matrix, walking_dist, need_return)
        end = time.time()
        print('OR calculation time is {}'.format(end - start), flush=True)

        return route
