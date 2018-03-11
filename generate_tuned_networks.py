
from functions import ( generate_aniso_network,
                        Tuned_netw_dist_profile )
from params.generate_tuned_networks_params import *
from generate_tuned_networks_label import label

import numpy as np


np.random.seed(seed)


tn_ddcp = Tuned_netw_dist_profile()

for i in range(n_graphs):
    spath = "/home/lab/comp/data/" + label \
            +"-"+"%.2d" % i +".gt"
    generate_aniso_network(N, tn_ddcp.C, ed_l, spath)
                           
