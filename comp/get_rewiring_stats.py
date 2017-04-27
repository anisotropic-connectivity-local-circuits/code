
from functions import rewire
from params.get_rewiring_stats_params import *
from get_rewiring_stats_label import label

import graph_tool as gt
import sys, uuid, os, pickle


for gpath in sys.argv[1:-1]:
    gid = os.path.splitext(gpath)[0][-4:]
    g = gt.load_graph(gpath)
    h, stat = rewire(g, rew_frac, eps_f)
    spath = "/home/lab/data/"+label+"-"+gid
    with open(spath+".p", "wb") as pfile:
        pickle.dump(stat,pfile)


                           
