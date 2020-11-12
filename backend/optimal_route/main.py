# -*- coding: utf-8 -*-
import plot_tools as pt
import osmp_tools as ost
from optimizer import Optimizer

berlinCenter = (52.5198810, 13.4073380)
#berlinCenter = (52.512, 13.3912)


def main():
    time_for_route = 180
    points_of_interest = ost.get_berlin_cafes()
    need_return = True

    opt = Optimizer()
    route, paths = opt.solve(berlinCenter, points_of_interest, time_for_route, need_return=need_return)
    pt.plot_routing_path(points_of_interest, opt.og, route, paths)


if __name__ == '__main__':
    main()
