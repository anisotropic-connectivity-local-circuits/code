
import graph_tool as gt
import numpy as np

from network_building import distribute_neurons_randomly
from network_eval import get_dist_matrix


def connect_dist_network(g, d):

    D = get_dist_matrix(g)

    for i in range(len(D)):
        for j in range(len(D)):
            if not i == j:
                if np.random.uniform() < d(D[i][j]):
                    g.add_edge(g.vertex(i),g.vertex(j))

    return g



def generate_dist_network(N, d, ed_l, save_path = ''):

    ''' 
    d:   function that takes one value (distance) and
         returns connection probability 
    '''

    g = gt.Graph()

    # store graph attributes
    graph_type = g.new_graph_property("string")
    graph_type[g] = "dist_depend"
    g.graph_properties["graph_type"] = graph_type

    edge_length = g.new_graph_property("double")
    edge_length[g] = ed_l
    g.graph_properties["ed_l"] = edge_length

    rewired = g.new_graph_property("bool")
    rewired[g] = False
    g.graph_properties["rewired"] = rewired

    self_loops = g.new_graph_property("bool")
    self_loops[g] = False
    g.graph_properties["self_loops"] = self_loops

    parallel_edges = g.new_graph_property("bool")
    parallel_edges[g] = False
    g.graph_properties["parallel_edges"] = parallel_edges

    # add vertices and a random position for each vertex
    positions = distribute_neurons_randomly(N, ed_l)     
    xy = g.new_vertex_property("vector<double>")
    for k in range(N):
        g.add_vertex()
        xy[g.vertex(k)] = list(positions[k])
    g.vertex_properties["xy"] = xy

    g = connect_dist_network(g, d) 

    if not save_path == '':
        g.save(save_path) 
        print "Graph saved to \n\t%s\n" %(save_path)

    return g





