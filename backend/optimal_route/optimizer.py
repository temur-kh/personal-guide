import route_tools as rt

import nx_tools as nxt
import data as dt
import osmp_tools as ost
import time


class Optimizer:
    speed = 0.1  # km/min

    def __init__(self, graph=None):
        self.og = graph
        return

    def estimate_graph_distance_from_walking_dist(self, d):
        return 5000

    def estimate_walking_distance_from_time(self, t):
        """
            Having time in minutes, estimate distance in km
        """

        return Optimizer.speed * t

    def solve(self, starting_point, points_of_interest, time_for_route):
        walking_dist = self.estimate_walking_distance_from_time(time_for_route)
        graph_dist = self.estimate_graph_distance_from_walking_dist(walking_dist)

        if self.og is None:
            print('create_graph ...')
            self.og = nxt.create_graph(starting_point[0], starting_point[1], graph_dist)

        ost.set_start_coords(starting_point[0], starting_point[1])
        ost.set_map_distance(walking_dist)

        print('find_nodes_in_graph')
        poi_ids = nxt.find_nodes_in_graph(self.og, points_of_interest)
        starting_point_id = nxt.find_node_in_graph(self.og, starting_point)

        start = time.time()
        poi_paths = nxt.dijkstra_all_paths_for_list(self.og.graph, poi_ids)
        end = time.time()
        print('Points of interest: dijkstra time {}'.format(end - start))

        new_point = nxt.dijkstra_paths_for_point(self.og.graph, poi_paths, poi_ids, starting_point_id)

        if new_point:
            dt.add_new_starting_point(points_of_interest, starting_point, starting_point_id)

        distances = rt.fill_distance_matrix(points_of_interest, poi_paths)

        start = time.time()
        routes = rt.test_ortools(points_of_interest, distances=True, hard=True)
        end = time.time()
        print('OR calculation time is {}'.format(end - start))

        return routes, poi_paths

