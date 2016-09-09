
import graph_tool as gt
import numpy as np

def mock_test():
    return True


def distribute_neurons_randomly(N, ed_l):
    return np.random.uniform(0,ed_l, (N, 2))


def generate_aniso_network(N, w, ed_l = 212., save_path = '',
                           with_self_loops = True, with_parallel_edges = True):
    '''
    '''
    

    g = gt.Graph()
    
    # store graph attributes

    graph_type = g.new_graph_property("string")
    graph_type[g] = "anisotropic"
    g.graph_properties["graph_type"] = graph_type   

    edge_length = g.new_graph_property("double")
    edge_length[g] = ed_l
    g.graph_properties["ed_l"] = edge_length

    rewired = g.new_graph_property("bool")
    rewired[g] = False
    g.graph_properties["rewired"] = rewired

    self_loops = g.new_graph_property("bool")
    self_loops[g] = with_self_loops
    g.graph_properties["self_loops"] = self_loops

    parallel_edges = g.new_graph_property("bool")
    parallel_edges[g] = with_parallel_edges
    g.graph_properties["parallel_edges"] = parallel_edges

    # add vertices and a random position for each vertex

    positions = distribute_neurons_randomly(N, ed_l) 
    
    xy = g.new_vertex_property("vector<double>")
    axon_angle = g.new_vertex_property("double")

    for k in range(N):
        g.add_vertex()
        xy[g.vertex(k)] = positions[k]

    g.vertex_properties["xy"] = xy

    return g
