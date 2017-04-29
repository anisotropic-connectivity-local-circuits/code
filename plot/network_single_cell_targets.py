
import matplotlib as mpl
mpl.use('Agg')
import pylab as pl



def plot_network_single_cell_targets(g, i, save_path,
                                     color = '#1f78b4'):

    pl.clf()
    fig = pl.figure()
    fig.set_size_inches(3.,3.)
    
    ax = fig.add_subplot(111)

    xy = g.vertex_properties["xy"]
    xs = [xy[v][0] for v in g.vertices()]
    ys = [xy[v][1] for v in g.vertices()]

    source = g.vertex(i)
    target_ids = []
    for e in source.out_edges():
        target_ids.append(int(e.target()))

    target_xs = [xs[k] for k in target_ids]
    target_ys = [ys[k] for k in target_ids]

    ax.plot(xs,ys, 'o', color='k', markersize=0.5,)
    ax.plot(target_xs, target_ys, 'o', color='r',
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



import graph_tool as gt
g = gt.load_graph('../data/N1000_w126_manual-rew.gt')
plot_network_single_cell_targets(g, 0, '../img/new2.png',
                                     color = '#1f78b4')
