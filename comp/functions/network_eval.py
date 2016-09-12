
import numpy as np
import graph_tool as gt


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
    |u_i - u_j| = \sqrt{ <u_i - u_j, ui - u_j>}
     = \sqrt{<u_i,u_i> + <u_j,u_j> - 2<u_i,u_j>}
     = \sqrt{r_ij - 2 s_ij}
    
    Compute r_ij = <u_i,u_i> + <u_j,u_j> and
            s_ij = <u_i,u_j> separately 
    and finally get distances as
            D_ij = \sqrt{r_ij - 2 s_ij}.
    '''
    
    N = g.num_vertices()
  
    xs,ys = get_xy(g)

    # [[2.56,18.79,...],[25.12,9.48,...]]
    # into
    # [[2.56,25.12],[18.79, 9.48],...]
    xy = np.array([xs,ys]).T

    # construct the matrix r_ij = <u_i,u_j> 
    r = np.dot(xy,xy.transpose())
    assert( np.shape(r) == (N,N))

    # construct the matrix s_ij = <u_i,u_i>+<u_j,u_j>
    norms = np.sum( xy**2. , axis = 1  )
    tmp = np.reshape(norms.repeat(N),(N,N))
    s = tmp + tmp.transpose()

    # last step
    distances = (s - 2*r)**0.5

    return distances
