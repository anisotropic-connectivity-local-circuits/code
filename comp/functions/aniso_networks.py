
import graph_tool as gt
import numpy as np


def distribute_neurons_randomly(N, ed_l):
    return np.random.uniform(0,ed_l, (N, 2))

def rotate(alpha, positions):
    rot_matrix = np.array([[np.cos(alpha), -np.sin(alpha)],
                           [np.sin(alpha),np.cos(alpha)]])

    return np.array([np.dot(rot_matrix,np.transpose(pos))
                     for pos in positions])


def find_axon_targets(i, alpha, positions, w):    
    '''
    i: index of source neuron
    alpha: axon direction
    positions: matrix of positions
    '''

    targets = []
    
    npositions = rotate(alpha, positions - positions[i])
    
    for k, pos in enumerate(npositions):
        ylim = w(pos[0])
        if -ylim <= pos[1] <= ylim and 0 < pos[0]:
            targets.append(k)
        
    return targets


def connect_graph(g, i, targets):
    for j in targets:
        g.add_edge(g.vertex(i), g.vertex(j))
    return g


def generate_aniso_network(N, w, ed_l = 212., save_path = ''):
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
        deg = np.random.randint(0,36000)/100.
        #sys.stdout.write("\rAlpha: %.2f;\t %d of %d;\t %.2f%%" % (a_deg,base_index,N,base_index/float(N)*100))
        #sys.stdout.flush()
        alpha = deg/180. * np.pi
        targets = find_axon_targets(i, alpha, positions, w)
        axon_angle[g.vertex(i)] = alpha
        g = connect_graph(g, i, targets)

    g.vertex_properties["alpha"] = axon_angle
        
    return g
