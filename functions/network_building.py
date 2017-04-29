
import numpy as np


def distribute_neurons_randomly(N, ed_l):
    return np.random.uniform(0,ed_l, (N, 2))


def connect_graph(g, i, targets):
    for j in targets:
        g.add_edge(g.vertex(i), g.vertex(j))
    return g
