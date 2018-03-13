
from functions import rewire
from params.rewire_networks_params import *
from rewire_networks_repeatedly_label import label

import graph_tool as gt
import sys, os, pickle

import numpy as np

np.random.seed(seed)


for gpath in sys.argv[1:-1]:
    gid = os.path.splitext(gpath)[0][-2:]
    g = gt.load_graph(gpath)
    h1, stat = rewire(g , rew_frac, eps_f)
    h2, stat = rewire(h1, rew_frac, eps_f)
    h3, stat = rewire(h2, rew_frac, eps_f)
    h4, stat = rewire(h3, rew_frac, eps_f)
    h5, stat = rewire(h4, rew_frac, eps_f)
    h6, stat = rewire(h5, rew_frac, eps_f)
    h7, stat = rewire(h6, rew_frac, eps_f)
    h8, stat = rewire(h7, rew_frac, eps_f)
    h9, stat = rewire(h8, rew_frac, eps_f)
    h10, stat = rewire(h9, rew_frac, eps_f)
    
    spath = "/home/lab/comp/data/"+label+"_r2_"+"-"+gid
    h2.save(spath+".gt")
    spath = "/home/lab/comp/data/"+label+"_r5_"+"-"+gid
    h5.save(spath+".gt")
    spath = "/home/lab/comp/data/"+label+"_r10_"+"-"+gid
    h10.save(spath+".gt")
                           
