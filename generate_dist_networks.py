
from functions import ( generate_dist_network,
                        Aniso_netw_dist_profile )
from params.generate_dist_networks_params import *
from generate_dist_networks_label import label

import numpy as np

np.random.seed(seed)

an_ddcp = Aniso_netw_dist_profile(w)

for i in range(n_graphs):
    spath = "/home/lab/comp/data/" + label \
            +"-"+"%.2d" % i +".gt"
    generate_dist_network(N, an_ddcp.C, ed_l, spath)
                           
