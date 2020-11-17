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


def plot_routing_path(data, og, route, paths):
    plt.figure(figsize=(8, 6))
    fig = plt.figure()
    total_len = 0
    lons = []
    lats = []
    points_lons = []
    points_lats = []
    nv = len(route) - 1
    for iv in range(nv):
        jv = iv + 1
        # get path between iv and jv
        i_id_in_map = data['ids'][route[iv]]
        j_id_in_map = data['ids'][route[jv]]
        path = paths[i_id_in_map][j_id_in_map].get_path()
        len_path = paths[i_id_in_map][j_id_in_map].get_distance()
        total_len += len_path

        for p in path:
            lons.append(og.pos[p][0])
            lats.append(og.pos[p][1])

    for iv in range(nv + 1):
        i_id_in_map = data['ids'][route[iv]]
        points_lons.append(og.pos[i_id_in_map][0])
        points_lats.append(og.pos[i_id_in_map][1])

    other_points_lons = []
    other_points_lats = []
    for iv in range(data['nv']):
        if iv in route:
            continue
        i_id_in_map = data['ids'][iv]
        other_points_lons.append(og.pos[i_id_in_map][0])
        other_points_lats.append(og.pos[i_id_in_map][1])

    print(f'Total path length = {total_len}')
    print(f'Number of visited nodes = {nv}')
    plt.plot(lons, lats, linewidth=4)
    plt.plot(points_lons, points_lats, 'ro', markersize=10)
    plt.plot(other_points_lons, other_points_lats, 'go', markersize=10)
    mplleaflet.show(fig=fig)

