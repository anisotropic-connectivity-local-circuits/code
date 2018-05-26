
from functions import get_2neuron_counts
import graph_tool as gt

from get_two_motifs_label import label
from params.get_two_motifs_params import *

import pickle, os, sys

import numpy as np

data = {}

for gpath in sys.argv[1:-1]:

    g = gt.load_graph(gpath)
    uc, sc, rc = get_2neuron_counts(g)

    gid = os.path.splitext(os.path.basename(gpath))[0][-2:]
    data[gid]=[uc,sc,rc]


fpath = "data/two_motif_counts_" \
        + "{:s}.p".format(graph_type)

with open(fpath, "wb") as pfile:
    pickle.dump(data, pfile)
    


    
    



    
