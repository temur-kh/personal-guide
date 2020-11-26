import route_tools as rt
import data as dt
import time
import multiprocessing as multi
import numpy as np

#multi.set_start_method('fork', force=True)

MAX_DISTANCE_IN_MAP = 10000


def correct_distance_matrix_no_return(data):
    depot = data['depot']
    nv = data['nv']
    distance_matrix = data['distance_matrix']
    print(f'depot = {depot}, nv = {nv}')
    for i in range(nv):
        distance_matrix[i][depot] = 0


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
                nv - число вершин
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)

        if not need_return:
            correct_distance_matrix_no_return(data)

        distance_matrix = data['distance_matrix']

        USE_OR_HEURISTIC = False

        start = time.time()
        if USE_OR_HEURISTIC:
            route = rt.find_route_with_distance_limit(data, distance_matrix, walking_dist,
                                                      need_return, hard=True)
        else:
            route, route_distance = rt.reward_collecting_tsp(data, distance_matrix, walking_dist)
        end = time.time()
        print('OR calculation time is {}'.format(end - start), flush=True)
        if not need_return:
            route.pop()

        return route

    def solve_clusters(self, data, clusters, time_for_route, need_return=False):

        """
            data - словарь с ключами:
                distance_matrix - матрица расстояний между всеми точками
                depot - индекс стартовой вершины
                nv - число вершин
            clusters - списки с индексами вершин
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)
        all_route_dist = 0
        all_route = []
        starting_point = data['depot']
        for cluster in clusters:
            cluster_data = dt.extract_data(data, cluster, starting_point)
            print(cluster_data)
            if not need_return:
                correct_distance_matrix_no_return(cluster_data)
            distance_matrix = cluster_data['distance_matrix']
            route, route_distance = rt.reward_collecting_tsp(cluster_data, distance_matrix,
                                                             walking_dist - all_route_dist)
            if not need_return:
                route.pop()
            if len(all_route) > 0:
                all_route.pop()

            for r in route:
                all_route.append(cluster[r])
                print(cluster[r])

            all_route_dist += route_distance
            starting_point = all_route[-1]
            if all_route_dist >= walking_dist:
                break

        print(f'total distance = {all_route_dist}')
        return all_route

    def solve_worker(self, id, n_processes, data, clusters, time_for_route, need_return):
        if id == 0:
            return self.solve(data, time_for_route, need_return)
        else:
            return self.solve_clusters(data, clusters, time_for_route, need_return)

    def solve_parallel(self, data, clusters, time_for_route, need_return=False):
        n_processes = 2  # multi.cpu_count()
        pool = multi.Pool(n_processes)

        results = [
            pool.apply_async(self.solve_worker, args=(id, n_processes, data, clusters, time_for_route, need_return))
            for id in range(n_processes)]

        routes = [p.get() for p in results]
        pool.close()

        return routes
