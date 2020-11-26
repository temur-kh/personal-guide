# -*- coding: utf-8 -*-
import plot_tools as pt
import osmp_tools as ost
import data as dt
from optimizer import Optimizer

berlinCenter = (52.5198810, 13.4073380)
#berlinCenter = (52.512, 13.3912)


def main():
    time_for_route = 100  # minutes
    speed = 100  # meters in minute
    need_return = False

    data = dt.create_data_model_distance()

    nclusters = 2
    clusters = dt.create_clusters(data['nv'], nclusters)
    print(clusters)

    opt = Optimizer(speed=speed)
    #route = opt.solve(data, time_for_route, need_return=need_return)
    #route = opt.solve_clusters(data, clusters, time_for_route, need_return=need_return)
    routes = opt.solve_parallel(data, clusters, time_for_route, need_return)

    print('final route:')
    for route in routes:
        print(route)


if __name__ == '__main__':
    main()