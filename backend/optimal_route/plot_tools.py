# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import mplleaflet


def plot_nodes(data, routes):
    plt.figure(figsize=(8, 6))
    fig = plt.figure()
    for i, route in enumerate(routes):
        lons = []
        lats = []
        for r in route:
            lons.append(data['lons'][r])
            lats.append(data['lats'][r])
        plt.plot(lons, lats)
        plt.plot(lons, lats, 'ro')
        mplleaflet.show(fig=fig)
        # mplleaflet.display(fig=fig)

def plot_path(data, og, path):
    plt.figure(figsize=(8, 6))
    fig = plt.figure()

    lons = []
    lats = []
    for p in path:
        lons.append(og.pos[p][0])
        lats.append(og.pos[p][1])

    print(len(lons), len(lats))
    plt.plot(lons, lats)
    plt.plot(lons, lats, 'ro')
    mplleaflet.show(fig=fig)
    # mplleaflet.display(fig=fig)


def plot_routing_path(data, og, routes, paths, back=False):
    plt.figure(figsize=(8, 6))
    fig = plt.figure()
    for i, route in enumerate(routes):
        lons = []
        lats = []
        points_lons = []
        points_lats = []
        nv = data['nv'] #len(route) - 1
        print(f'nv = {nv}')
        route_nv = nv if back else nv - 1
        for iv in range(route_nv):
            jv = iv + 1
            # get path between iv and jv
            i_id_in_map = data['ids'][route[iv]]
            j_id_in_map = data['ids'][route[jv]]
            path = paths[i_id_in_map][j_id_in_map].get_path()

            for p in path:
                lons.append(og.pos[p][0])
                lats.append(og.pos[p][1])

        for iv in range(nv):
            points_lons.append(data['lons'][iv])
            points_lats.append(data['lats'][iv])

        plt.plot(lons, lats, linewidth=4)
        plt.plot(points_lons, points_lats, 'ro', markersize=10)
        mplleaflet.show(fig=fig)

