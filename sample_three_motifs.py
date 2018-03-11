
from functions import sample_three_motifs
import graph_tool as gt

from params.sample_three_motifs_params import *
from sample_three_motifs_label import label

import pickle, os, sys

import numpy as np

np.random.seed(seed)

data = {}
for gpath in sys.argv[1:-1]:
    g = gt.load_graph(gpath)
    motif_counts = sample_three_motifs(g, sample_size)
    gid = os.path.splitext(os.path.basename(gpath))[0][-2:]

    data[gid]=motif_counts

    fpath = "data/three_motif_counts_" \
            + "{:s}_S{:d}.p".format(graph_type, sample_size)

    with open(fpath, "wb") as pfile:
        pickle.dump(data, pfile)
    


    
    



    
