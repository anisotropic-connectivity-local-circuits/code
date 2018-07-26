
from functions import rewire, get_common_neighbours
from params.rewire_and_get_common_input_variance_params import *
from rewire_and_get_common_input_variance_label import label

import graph_tool as gt
import sys, uuid, os, pickle

import numpy as np

np.random.seed(seed)

n_graphs = len(sys.argv[1:-1])
rew_stages = np.linspace(0,1.0,n_rew_stages)

vars_all = np.zeros((n_graphs,n_rew_stages))
vars_unc = np.zeros((n_graphs,n_rew_stages))
vars_sng = np.zeros((n_graphs,n_rew_stages))
vars_bdr = np.zeros((n_graphs,n_rew_stages))

for j,gpath in enumerate(sys.argv[1:-1]):

    gid = os.path.splitext(gpath)[0][-2:]
    g = gt.load_graph(gpath)

    pairs, cn, in_nb, out_nb = get_common_neighbours(g)
    vars_all[j,0]+=np.var(in_nb)
    vars_unc[j,0]+=np.var(in_nb[cn==0])
    vars_sng[j,0]+=np.var(in_nb[cn==1])
    vars_bdr[j,0]+=np.var(in_nb[cn==2])

    for k,rew_frac in enumerate(rew_stages[1:]):

        h, stat = rewire(g, rew_frac, eps_f)

        pairs, cn, in_nb, out_nb = get_common_neighbours(h)
        vars_all[j,k+1]+=np.var(in_nb)
        vars_unc[j,k+1]+=np.var(in_nb[cn==0])
        vars_sng[j,k+1]+=np.var(in_nb[cn==1])
        vars_bdr[j,k+1]+=np.var(in_nb[cn==2])        
    

spath = "/home/lab/comp/data/"+label

vs = {'all': vars_all, 'unc': vars_unc,
      'sng': vars_sng, 'bdr': vars_bdr,
      'rew_stages': rew_stages}

with open(spath+".p", "wb") as pfile:
    pickle.dump(vs,pfile)

                           
