
from functions import generate_aniso_network
from params.generate_aniso_networks_params import *
from generate_aniso_networks_label import label

import numpy as np

np.random.seed(seed)

w_f = lambda x: w

for i in range(n_graphs):
    spath = "/home/lab/comp/data/" + label \
            +"-"+str(i)+".gt"
    generate_aniso_network(N, w_f, ed_l, spath)
                           
