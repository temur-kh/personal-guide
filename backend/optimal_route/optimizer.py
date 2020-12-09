try:
    from . import data as dt
    from . import route_tools as rt
except:
    import data as dt
    import route_tools as rt
import time
import multiprocessing as multi

# multi.set_start_method('fork', force=True)

MAX_DISTANCE_IN_MAP = 10000


def correct_distance_matrix_no_return(data):
    depot = data['depot']
    nv = data['nv']
    distance_matrix = data['distance_matrix']
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

        return int(self.speed * t)

    def solve(self, data, time_for_route, need_return=False):

        """
            data(dict) - информациея о poi. Ключи:
                ids(list) - список id_osm.
                category(list) - список категорий poi.
                locations(list) - список координат poi в формате: [lat, lon].
                nv(int) - кол-во poi.
                num_vehicles(int)
                depot(int) - индекс(в ids) стартовой точки.
                constraints(dict) - словарь constraints с индексами(в ids):
                        {category_constraint: [], ...}
                distance_matrix(list) - матрица кратчайших расстояний(int), размером (nv, nv)
                rewards(list) - список наград для точек интереса.
            time_for_route - время на маршрут
            need_return = bool, нужно ли возвращаться в стартовую точку
        """
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)

        if not need_return:
            correct_distance_matrix_no_return(data)

        USE_OR_HEURISTIC = False
        start = time.time()
        if USE_OR_HEURISTIC:
            distance_matrix = data['distance_matrix']
            route = rt.find_route_with_distance_limit(data, distance_matrix, walking_dist,
                                                      need_return, hard=True)
        else:
            route, route_distance = rt.reward_collecting_tsp(data, walking_dist)
        end = time.time()
        print('OR calculation time is {}'.format(end - start), flush=True)
        if not need_return and len(route) > 1:
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
            if not need_return:
                correct_distance_matrix_no_return(cluster_data)
            route, route_distance = rt.reward_collecting_tsp(cluster_data,
                                                             walking_dist - all_route_dist)
            if len(route) == 0:
                return all_route

            if not need_return:
                route.pop()
            if len(all_route) > 0:
                all_route.pop()

            for r in route:
                all_route.append(cluster[r])
                print(cluster[r], flush=True)

            all_route_dist += int(route_distance)
            starting_point = all_route[-1]
            if all_route_dist >= walking_dist:
                break

        print(f'total distance = {all_route_dist}', flush=True)
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
        #results = [self.solve_worker(1, n_processes, data, clusters, time_for_route, need_return)]
        routes = [p.get() for p in results]
        pool.close()

        return routes
