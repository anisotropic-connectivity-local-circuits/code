
import graph_tool as gt
import numpy as np

from network_building import distribute_neurons_randomly
from network_building import connect_graph


def rotate(alpha, positions):
    rot_matrix = np.array([[np.cos(alpha), -np.sin(alpha)],
                           [np.sin(alpha),np.cos(alpha)]])
    return np.array([np.dot(rot_matrix,np.transpose(pos))
                     for pos in positions])


def find_axon_targets(i, alpha, positions, w):    
    '''
    Finds the target nodes for a neuron with index "i", 
    axon orientation "alpha", axon width function "w" 
    in a network with neuros located at "positions".
    --------------------------------------------------
    i:           index of source neuron
    alpha:       axon direction
    positions:   array of node positions
    w:           function returning the axon width/2
    '''

    targets = []    
    npositions = rotate(-alpha, positions - positions[i])
    
    for k, pos in enumerate(npositions):
        ylim = w(pos[0])
        if -ylim <= pos[1] <= ylim and 0 < pos[0]:
            targets.append(k)
        
    return targets


def generate_aniso_network(N, w, ed_l, save_path = ''):
    '''
    Generates a (tuned) anisotropic network.
    --------------------------------------------------
    N:    Number of neurons
    w:    Axon-width function. Takes a single value x, 
          the axon distance, and returns the half-width of 
          the "axon-band" at this length.
          If w returns a single value (w = lambda x: c),
          the network is refered to as "anisotropic", 
          otherwise "tuned anisotropic".
    ed_l: Edge length of the quadratic surface area of 
          the network
    '''
    
    g = gt.Graph()
    
    # store graph attributes
    graph_type = g.new_graph_property("string")
    if w(0)==w(ed_l/2.)==w(ed_l):
        graph_type[g] = "aniso"
    else:
        graph_type[g] = "tuned_aniso"
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

    # add axon angle for each vertex and connect
    axon_angle = g.new_vertex_property("double")
    for i in range(N):
        alpha = np.random.uniform(0,2*np.pi)
        axon_angle[g.vertex(i)] = alpha
        targets = find_axon_targets(i, alpha, positions, w)
        g = connect_graph(g, i, targets)

    g.vertex_properties["alpha"] = axon_angle

    if not save_path == '':
        g.save(save_path) 
        print "Graph saved to: %s" %(save_path)
        
    return g
