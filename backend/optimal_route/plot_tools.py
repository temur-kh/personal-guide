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
    for r in path:
        lons.append(og.pos[r][0])
        lats.append(og.pos[r][1])
        #print(og.pos[r][0], og.pos[r][1])

    print(len(lons), len(lats))
    plt.plot(lons, lats)
    plt.plot(lons, lats, 'ro')
    mplleaflet.show(fig=fig)
    # mplleaflet.display(fig=fig)