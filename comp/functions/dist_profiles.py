
import numpy as np


def aniso_netw_dist_profile(x, w):
    '''
    Distance-dependent connection probability profile of 
    the anisotropic network with axon width 2w as derived 
    in the supporting information
    --------------------------------------------------
    x  : inter-neuron distance
    w  : half-width of the axon
    '''

    assert(x>=0)

    if x < w:
        return 0.5
    else:
        return 1/(np.pi) * np.arcsin(2*w/(2*x))
        
