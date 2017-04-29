
import graph_tool as gt
import numpy as np
import random

from functions import get_dist_matrix

def rewire(g, rew_frac=1., eps_f=0.05):
    '''
    Rewire a given graph while preserving the 
    distance-dependent connectivity profile
    --------------------------------------------------
    g        : graph to rewire
    fraction : fraction of edges that get rewired
    eps_f    : margin for rewiring specified as 
               a fraction of the graph's ed_l
    '''

    ed_l = g.graph_properties["ed_l"]
    eps = (ed_l * eps_f)/2.

    h = gt.Graph(g)
    h.clear_edges()

    D = get_dist_matrix(g)

    rew_stat = {}
    fail_edges = []

    for v in g.vertices():

        to_rewire = []
        remain_unchanged = []

        for out_e in v.out_edges():

            if np.random.uniform() <= rew_frac:    
                to_rewire.append(out_e)
            else:
                remain_unchanged.append(out_e)

        # connect unchanged edges first, those are not
        # suitable targets for rewiring anymore
        for out_e in remain_unchanged:
            h.add_edge(v, out_e.target())

        for out_e in to_rewire:

            #find suitable new target
            d = D[int(out_e.source()),int(out_e.target())]
            rew_opts = np.where(
                np.logical_and((d-eps) <= D[int(v)],
                               D[int(v)] <= (d+eps)))[0]

            rew_stat[(int(v), int(out_e.target()))] = len(rew_opts)

            new_target = random.choice(rew_opts)

            target_valid = True
            rew_tries = 0

            while (bool(h.edge(v,h.vertex(new_target))) or
                   int(v)==new_target):
            # if edge already exists, whether because it was an
            # unchanged edge (rew_frac < 1)or it has been chosen as
            # a rewiring target for the same v, or v is supposed to
            # connect to itsef (can only happen if d < eps), chose
            # other new target

                rew_tries += 1
                if rew_tries > len(rew_opts)/2.:
                    fail_edges.append((int(v), int(out_e.target())))
                    target_valid = False
                    break

                new_target = random.choice(rew_opts)

            if target_valid:
                h.add_edge(h.vertex(int(v)),h.vertex(new_target))
    

         
    print 'Failed to rewire {:d} out of {:d} edges'.format(
        len(fail_edges), int(g.num_edges()))

    statistics = {"rew_stat":rew_stat, "fail_edges":fail_edges}

    h.graph_properties["rewired"] = h.new_graph_property("bool",
                                                         True)
    
    return h, statistics    

