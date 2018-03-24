
import numpy as np
import graph_tool as gt
from collections import defaultdict
from scipy.spatial import distance_matrix as scipy_distance_matrix


def eval_connectivity(g):
    '''
    works only when no parallel edges!   
    '''
    numer = float(g.num_edges())
    denom = g.num_vertices()*(g.num_vertices()-1.)
    
    return numer/denom


def get_xy(g):
    '''
    return x and y coordinates of the vertices
    '''

    xy = g.vertex_properties["xy"]

    xs = [xy[v][0] for v in g.vertices()]
    ys = [xy[v][1] for v in g.vertices()]

    return xs,ys


def get_target_ids(g, i):

    source = g.vertex(i)
    targets = []

    for e in source.out_edges():
        targets.append(int(e.target()))

    return targets



def get_dist_matrix(g):
    '''
    use scipy's distance_matrix to get matrix of 
    distances in graph.

    Example:
      two nodes [0.,0.] and [1.,1.] in graph, then
    
      distances =  array([[ 0.        ,  1.41421356],
                          [ 1.41421356,  0.        ]])

    '''
  
    xs,ys = get_xy(g)

    # turn
    #     [[2.56,18.79,...],[45.12,9.48,...]]
    # into
    #     [[2.56,45.12],[18.79, 9.48],...]
    xy = np.array([xs,ys]).T

    distances = scipy_distance_matrix(xy, xy)

    return distances


def get_adjacency_matrix(g):
    '''
                  presynaptic 
               -----------------
    post-     |                 |
    synaptic  |                 |     
              |                 |    

    '''

    N = g.num_vertices()
    A = np.zeros((N,N))

    for v in g.vertices():
        for e in v.out_edges():
            A[int(e.target())][int(v)] = 1

    return A


def get_dists_of_connected_pairs(g):

    D = get_dist_matrix(g)
    A = get_adjacency_matrix(g)
    
    return D[np.where(A==1)]


def get_ddcp(g, bins):
    '''
    get distance dependent connectivity profile
    --------------------------------------------------
    g:           input graph
    bins:        int or list, bins for profile
    '''

    D = get_dist_matrix(g)
    d_cp = D[np.where(get_adjacency_matrix(g)==1)]

    d_frq, bins = np.histogram(D.flatten(), bins)
    d_cp_frq, bins = np.histogram(d_cp, bins)

    centers = (bins[:-1]+bins[1:])/2.

    return centers, d_cp_frq/d_frq.astype(np.float)


def get_2neuron_p(g):
    '''
    get the probabilities for the three connection
    types (unconnected, single connection, reciprocal)
    for a random neuron pair in the network
    --------------------------------------------------
    arguments
        g:           input graph

    returns
        uc  -  probability for unconnected
        sc  -  probability for single connection
        bc  -  probability for reciprocal connectio
    '''
    N = g.num_vertices()
    A = get_adjacency_matrix(g)
    U = (A+A.T)[np.triu_indices(N,1)]

    uc = len(U[np.where(U==0)])
    sc = len(U[np.where(U==1)])
    bc = len(U[np.where(U==2)])

    T = float(uc+sc+bc)

    return uc/T, sc/T, bc/T    



def get_nmotif_ecounts(g, motif_size, sample_size):
    '''
    sample the number of edges in a random motif of size n
    --------------------------------------------------
    arguments
        g           :  input graph
        motif_size  :  size n of motifs (no. edges) to sample from
        sample_size :  total number of samples

    returns
        counter     :  counts of sampled motifs for given
                       number of edges
    '''

    counter = defaultdict(int)
    
    N = g.num_vertices()

    for k in range(sample_size):

        vertex_ids = np.array([])
        while len(np.unique(vertex_ids)) < motif_size:
            vertex_ids = np.random.randint(0, N, motif_size)

        is_part_of_motif = g.new_vertex_property("bool")

        for v_id in vertex_ids:
            is_part_of_motif[g.vertex(v_id)] = True

        g.set_vertex_filter(is_part_of_motif)

        ne = g.num_edges()
        
        counter[ne]+=1

        g.set_vertex_filter(None)

    return counter
