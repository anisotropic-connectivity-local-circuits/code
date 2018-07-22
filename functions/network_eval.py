
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

    N = g.num_vertices()
    D = get_dist_matrix(g)

    # distances of non-identical pairs
    dists = np.concatenate((D[np.triu_indices(N,1)],
                            D[np.tril_indices(N,-1)]))

    # adjacency of non-identical pairs
    A = get_adjacency_matrix(g)
    adj = np.concatenate((A[np.triu_indices(N,1)],
                          A[np.tril_indices(N,-1)]))

    # connection where adj=1
    d_cp = dists[np.where(adj==1)]

    d_frq, bins = np.histogram(dists, bins)
    d_cp_frq, bins = np.histogram(d_cp, bins)

    centers = (bins[:-1]+bins[1:])/2.

    return centers, d_cp_frq/d_frq.astype(np.float)


def get_dd_recip_p(g, bins):
    '''
    get distance dependent probabilities for reciprocal
    conections
    --------------------------------------------------
    arguments
        g:       input graph
        bins:    int or list, bins for profile

    returns
        x:       pair distance
        p(x):    estimated probability for a reciprocal
                 connection for a pair of nodes with
                 distance x                   
    '''

    N = g.num_vertices()
    D = get_dist_matrix(g)
    A = get_adjacency_matrix(g)
    
    # entries with in U with value 2 are recip. pairs
    #        |   1 0 1 2 |
    #        |     1 2 0 |
    # U =    |       0 1 |
    #        |         0 |
    #        |           |
    U = (A+A.T)[np.triu_indices(N,1)]
    D_triu = D[np.triu_indices(N,1)]
    d_rcp = D_triu[np.where(U==2)]

    d_frq, bins = np.histogram(D_triu, bins)
    d_rcp_frq, bins = np.histogram(d_rcp, bins)

    centers = (bins[:-1]+bins[1:])/2.

    return centers, d_rcp_frq/(d_frq.astype(np.float))


def get_2neuron_counts(g):
    '''
    get the counts for the three connection
    types (unconnected, single connection, reciprocal)
    for every unordered pair in the network
    --------------------------------------------------
    arguments
        g:           input graph

    returns
        uc  -  unconnected count
        sc  -  single connection count
        rc  -  reciprocal connection count
    '''
    N = g.num_vertices()
    A = get_adjacency_matrix(g)
    U = (A+A.T)[np.triu_indices(N,1)]

    uc = len(U[np.where(U==0)])
    sc = len(U[np.where(U==1)])
    rc = len(U[np.where(U==2)])

    return uc, sc, rc    


def get_2neuron_p(g):
    '''
    get the probabilities for the three connection
    types (unconnected, single connection, reciprocal)
    for a random neuron pair in the network
    --------------------------------------------------
    arguments
        g:           input graph

    returns
        up  -  probability for unconnected
        sp  -  probability for single connection
        rp  -  probability for reciprocal connection
    '''

    uc, sc, rc = get_2neuron_counts(g)
    
    T = float(uc+sc+rc)

    return uc/T, sc/T, rc/T



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


def get_common_neighbours(g):
    '''
    get the number of common in- and out-neighbours for 
    each pair of nodes in a graph
    --------------------------------------------------
    arguments
        g              :  input graph

    returns
        pairs          :  distinct unordered node pairs
        inn-neighbours :  number of common inputs of neuron
                          pair at same position in pairs
        out-neighbours :  number of common target of neuron
                          pair at same position in pairs
    '''

    N = g.num_vertices()
    A = get_adjacency_matrix(g)
    
    pairs, inn_neighbours, out_neighbours = [], [], []
    
    for i in range(N):
        for j in range(i+1,N):
            pairs.append((i,j))
            inn_neighbours.append(np.dot(A[i,:],A[j,:]))
            out_neighbours.append(np.dot(A[:,i],A[:,j]))

    return pairs, inn_neighbours, out_neighbours
    
    
