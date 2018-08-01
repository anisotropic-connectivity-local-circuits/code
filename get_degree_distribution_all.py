
from functions import ( generate_dist_network,
                        Tuned_netw_dist_profile,
                        generate_aniso_network,
                        Aniso_netw_dist_profile,
                        rewire )

from params.get_degree_distribution_all_params import *
from get_degree_distribution_all_label import label

import numpy as np
from scipy import stats


np.random.seed(seed)

tn_ddcp = Tuned_netw_dist_profile()
an_ddcp = Aniso_netw_dist_profile(w)
w_f = lambda x: w


all_nodes = range(N)

ind_aniso       = np.zeros((n_graphs,N))
ind_rew_aniso   = np.zeros((n_graphs,N))
ind_rew10_aniso = np.zeros((n_graphs,N))
ind_dist_aniso  = np.zeros((n_graphs,N))

oud_aniso       = np.zeros((n_graphs,N))
oud_rew_aniso   = np.zeros((n_graphs,N))
oud_rew10_aniso = np.zeros((n_graphs,N))
oud_dist_aniso  = np.zeros((n_graphs,N))

ind_tuned       = np.zeros((n_graphs,N))
ind_rew_tuned   = np.zeros((n_graphs,N))
ind_dist_tuned  = np.zeros((n_graphs,N))

oud_tuned       = np.zeros((n_graphs,N))
oud_rew_tuned   = np.zeros((n_graphs,N))
oud_dist_tuned  = np.zeros((n_graphs,N))



def in_degrees(g):
    return np.bincount(g.get_in_degrees(all_nodes).astype(np.int),
                       minlength=N)

def out_degrees(g):
    return np.bincount(g.get_out_degrees(all_nodes).astype(np.int),
                       minlength=N)


for i in range(n_graphs):

    g = generate_aniso_network(N, w_f, ed_l)
    ind_aniso[i,:]+=in_degrees(g)
    oud_aniso[i,:]+=out_degrees(g)

    h, stat = rewire(g, rew_frac, eps_f)
    ind_rew_aniso[i,:]+=in_degrees(h)
    oud_rew_aniso[i,:]+=out_degrees(h)

    h2, stat = rewire(h, rew_frac, eps_f)
    h3, stat = rewire(h2, rew_frac, eps_f)
    h4, stat = rewire(h3, rew_frac, eps_f)
    h5, stat = rewire(h4, rew_frac, eps_f)
    h6, stat = rewire(h5, rew_frac, eps_f)
    h7, stat = rewire(h6, rew_frac, eps_f)
    h8, stat = rewire(h7, rew_frac, eps_f)
    h9, stat = rewire(h8, rew_frac, eps_f)
    h10, stat = rewire(h9, rew_frac, eps_f)

    ind_rew10_aniso[i,:]+=in_degrees(h10)
    oud_rew10_aniso[i,:]+=out_degrees(h10)
  
    g = generate_dist_network(N, an_ddcp.C, ed_l)
    ind_dist_aniso[i,:]+=in_degrees(g)
    oud_dist_aniso[i,:]+=out_degrees(g)


    g = generate_aniso_network(N, tn_ddcp.C, ed_l)
    ind_tuned[i,:]+=in_degrees(g)
    oud_tuned[i,:]+=out_degrees(g)

    h, stat = rewire(g, rew_frac, eps_f)
    ind_rew_tuned[i,:]+=in_degrees(h)
    oud_rew_tuned[i,:]+=out_degrees(h)
  
    g = generate_dist_network(N, tn_ddcp.ddcp, ed_l)
    ind_dist_tuned[i,:]+=in_degrees(g)
    oud_dist_tuned[i,:]+=out_degrees(g)


    
data = {'in' : {'aniso'     : {'mean': np.mean(ind_aniso,axis=0),
                               'sem' : stats.sem(ind_aniso,axis=0)},
                'rew_aniso' : {'mean': np.mean(ind_rew_aniso,axis=0),
                               'sem' : stats.sem(ind_rew_aniso,axis=0)},
                'rew10_aniso' : {'mean': np.mean(ind_rew10_aniso,axis=0),
                                 'sem' : stats.sem(ind_rew10_aniso,axis=0)},
                'dist_aniso': {'mean': np.mean(ind_dist_aniso,axis=0),
                               'sem' : stats.sem(ind_dist_aniso,axis=0)},
                'tuned'     : {'mean': np.mean(ind_tuned,axis=0),
                               'sem' : stats.sem(ind_tuned,axis=0)},
                'rew_tuned' : {'mean': np.mean(ind_rew_tuned,axis=0),
                               'sem' : stats.sem(ind_rew_tuned,axis=0)},
                'dist_tuned': {'mean': np.mean(ind_dist_tuned,axis=0),
                               'sem' : stats.sem(ind_dist_tuned,axis=0)}},
        'out': {'aniso'     : {'mean': np.mean(oud_aniso,axis=0),
                               'sem' : stats.sem(oud_aniso,axis=0)},
                'rew_aniso' : {'mean': np.mean(oud_rew_aniso,axis=0),
                               'sem' : stats.sem(oud_rew_aniso,axis=0)},
                'rew10_aniso' : {'mean': np.mean(oud_rew10_aniso,axis=0),
                                 'sem' : stats.sem(oud_rew10_aniso,axis=0)},
                'dist_aniso': {'mean': np.mean(oud_dist_aniso,axis=0),
                               'sem' : stats.sem(oud_dist_aniso,axis=0)},
                'tuned'     : {'mean': np.mean(oud_tuned,axis=0),
                               'sem' : stats.sem(oud_tuned,axis=0)},
                'rew_tuned' : {'mean': np.mean(oud_rew_tuned,axis=0),
                               'sem' : stats.sem(oud_rew_tuned,axis=0)},
                'dist_tuned': {'mean': np.mean(oud_dist_tuned,axis=0),
                               'sem' : stats.sem(oud_dist_tuned,axis=0)}},
        'bin_vals': range(N)}


import pickle

spath = "/home/lab/comp/data/" + label
with open(spath+".p", "wb") as pfile:
    pickle.dump(data,pfile)

    
