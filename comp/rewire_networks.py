
from functions import rewire
from params.rewire_networks_params import *
from rewire_networks_label import label

import graph_tool as gt
import sys, uuid, os, pickle


for gpath in sys.argv[1:-1]:
    gid = os.path.splitext(gpath)[0][-4:]
    g = gt.load_graph(gpath)
    h, stat = rewire(g, rew_frac, eps_f)
    spath = "/home/lab/data/"+label+"-"+gid
    h.save(spath+".gt")
    with open(spath+"_stat.p", "wb") as pfile:
        pickle.dump(stat,pfile)


# for i in range(n_graphs):
#     spath = "/home/lab/data/"+label+"-"+str(uuid.uuid4())[:4]+".gt"
#     rewire(g, rew_frac=rew_frac, eps_f = eps_f)
                           
