
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


        
class Tuned_netw_dist_profile(object):
    '''
    Curve from Perin 2011
    '''

    def __init__(self):
        self.a = -1.4186123229540666E-03
        self.b = 2.7630272296832398E-03
        self.c = -9.4484523305731971E-01
        self.offset = 2.3078566917566815E-01

        
    def ddcp(self,x):
        if x==0.:
            return 0.230785669176
        else:
            return  self.a/(self.b+pow(x,self.c)) + self.offset

    def C(self,x):
        '''
        misnamed, should be w(x). see supplementary material
        for derivation
        '''

        return np.tan(self.ddcp(x)*np.pi)*x
