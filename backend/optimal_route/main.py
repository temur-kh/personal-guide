# -*- coding: utf-8 -*-
import numpy as np

import time

import route_tools as rt
import osmp_tools as ost
import plot_tools as pt
import nx_tools as nxt
import data as dt

#berlinCenter = (52.5198810, 13.4073380)
berlinCenter = (52.512, 13.3912)

def estimate_graph_distance_from_walking_dist(d):
    return 5000


def estimate_walking_distance_from_time(t):
    """
        Having time in minutes, estimate distance in km
    """

    speed = 0.1  # km/min
    return speed * t


def solve(starting_point, points_of_interest, time_for_route):
    walking_dist = estimate_walking_distance_from_time(time_for_route)
    graph_dist = estimate_graph_distance_from_walking_dist(walking_dist)

    print('create_graph ...')
    og = nxt.create_graph(starting_point[0], starting_point[1], graph_dist)

    ost.set_start_coords(starting_point[0], starting_point[1])
    ost.set_map_distance(walking_dist)

    print('find_nodes_in_graph')
    poi_ids = nxt.find_nodes_in_graph(og, points_of_interest)
    starting_point_id = nxt.find_node_in_graph(og, starting_point)

    start = time.time()
    poi_paths = nxt.dijkstra_all_paths_for_list(og.graph, poi_ids)
    end = time.time()
    print('Points of interest: dijkstra time {}'.format(end - start))

    new_point = nxt.dijkstra_paths_for_point(og.graph, poi_paths, poi_ids, starting_point_id)

    if new_point:
        print("new_point")
        dt.add_new_starting_point(points_of_interest, starting_point, starting_point_id)

    distances = rt.fill_distance_matrix(points_of_interest, poi_paths)

    start = time.time()
    routes = rt.test_ortools(points_of_interest, distances=True, hard=True)
    end = time.time()
    print('OR calculation time is {}'.format(end - start))

    pt.plot_routing_path(points_of_interest, og, routes, poi_paths, back=True)


def main():
    time_for_route = 180
    points_of_interest = ost.get_berlin_cafes()

    solve(berlinCenter, points_of_interest, time_for_route)


if __name__ == '__main__':
    main()
