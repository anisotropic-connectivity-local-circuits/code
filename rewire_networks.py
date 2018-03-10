
from functions import rewire
from params.rewire_networks_params import *
from rewire_networks_label import label

import graph_tool as gt
import sys, uuid, os, pickle

import numpy as np

np.random.seed(seed)


for gpath in sys.argv[1:-1]:
    gid = os.path.splitext(gpath)[0][-2:]
    g = gt.load_graph(gpath)
    h, stat = rewire(g, rew_frac, eps_f)
    spath = "/home/lab/comp/data/"+label+"-"+gid
    h.save(spath+".gt")
    with open(spath+"_stat.p", "wb") as pfile:
        pickle.dump(stat,pfile)

                           
