
from functions import ( generate_aniso_network,
                        Tuned_netw_dist_profile,
                        get_common_neighbours)

from params.get_common_input_distribution_tuned_params import *
from get_common_input_distribution_tuned_label import label

import numpy as np
from scipy import stats


np.random.seed(seed)

tn_ddcp = Tuned_netw_dist_profile()

bins = np.arange(0,N+binw,binw)
centers = 0.5*(bins[1:]+bins[:-1])

ci_unc = np.zeros((n_graphs, len(bins)-1))
ci_sng = np.zeros((n_graphs, len(bins)-1))
ci_bdr = np.zeros((n_graphs, len(bins)-1))

for i in range(n_graphs):
    
    g = generate_aniso_network(N, tn_ddcp.C, ed_l)

    pairs, cn, in_nb, out_nb = get_common_neighbours(g)

    ci_unc[i,:]+=np.histogram(in_nb[cn==0], bins, density=True)[0]
    ci_sng[i,:]+=np.histogram(in_nb[cn==1], bins, density=True)[0]
    ci_bdr[i,:]+=np.histogram(in_nb[cn==2], bins, density=True)[0]

    

spath = "/home/lab/comp/data/" + label

ci_s = {'centers': centers,
        'unc_means': np.mean(ci_unc, axis=0),
        'unc_sem'  : stats.sem(ci_unc, axis=0),
        'sng_means': np.mean(ci_sng, axis=0),
        'sng_sem'  : stats.sem(ci_sng, axis=0),
        'bdr_means': np.mean(ci_bdr, axis=0),
        'bdr_sem'  : stats.sem(ci_bdr, axis=0)}

import pickle

with open(spath+".p", "wb") as pfile:
    pickle.dump(ci_s,pfile)

    
