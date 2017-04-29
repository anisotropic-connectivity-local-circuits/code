
import numpy as np


class Aniso_netw_dist_profile(object):
    '''
    Struct to implement distance-dependent connection 
    probability profile. Initialize with axon half-width
    w and use C(x) to get the connection probability at 
    inter-neuron distance x.
    '''

    def __init__(self, w):
        self.w = w
        
    def C(self,x):
        '''
        Distance-dependent connection probability profile of 
        the anisotropic network with axon width 2w as derived 
        in the supporting information
        --------------------------------------------------
        x  : inter-neuron distance
        w  : half-width of the axon
        '''
        
        assert(x>=0)

        if x < self.w:
            return 0.5
        else:
            return 1/(np.pi) * np.arcsin(2*self.w/(2*x))


        
