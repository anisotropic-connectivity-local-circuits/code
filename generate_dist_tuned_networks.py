
from functions import ( generate_dist_network,
                        Tuned_netw_dist_profile )
from params.generate_dist_tuned_networks_params import *
from generate_dist_tuned_networks_label import label

import numpy as np

np.random.seed(seed)

tuned_ddcp = Tuned_netw_dist_profile()

for i in range(n_graphs):
    spath = "/home/lab/comp/data/" + label \
            +"-"+"%.2d" % i +".gt"
    generate_dist_network(N, tuned_ddcp.ddcp, ed_l, spath)
                           
