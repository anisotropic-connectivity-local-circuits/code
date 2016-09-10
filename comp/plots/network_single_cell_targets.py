
import matplotlib as mpl
mpl.use('Agg')
import pylab as pl

import graph_tool as gt

from functions import get_xy, get_target_ids


def plot_network_single_cell_targets(g, i, save_path,
                                     color = '#1f78b4'):

    pl.clf()
    fig = pl.figure()
    fig.set_size_inches(3.,3.)
    
    ax = fig.add_subplot(111)

    xs, ys = get_xy(g)

    target_ids = get_target_ids(g, i)

    xconnpos = [xs[k] for k in target_ids]
    yconnpos = [ys[k] for k in target_ids]

    ax.plot(xs,ys, 'o', color='k', markersize=0.5,)
    ax.plot(xconnpos,yconnpos, 'o', color='r',
            markerfacecolor= color, markeredgecolor= color,
            markersize = 3.)
    ax.plot(xs[i],ys[i], color = 'k', marker = '*', markersize= 13)

    ed_l = g.graph_properties["ed_l"]
    ax.set_xlim(0,ed_l)
    ax.set_ylim(0,ed_l)

    pl.xticks([])
    pl.yticks([])

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
   
    pl.savefig(save_path, dpi=300,  bbox_inches='tight')


