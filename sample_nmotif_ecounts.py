
from functions import get_nmotif_ecounts
import graph_tool as gt

from params.sample_nmotif_ecounts_params import *
from sample_nmotif_ecounts_label import label

import pickle, os, sys

import numpy as np

np.random.seed(seed)

data = {}
for gpath in sys.argv[1:-1]:
    g = gt.load_graph(gpath)
    ecounts = get_nmotif_ecounts(g, motif_size, sample_size)
    gid = os.path.splitext(os.path.basename(gpath))[0][-2:]

    data[gid]=ecounts

    fpath = "data/nmotif_ecounts_" \
            + "{:s}_n{:d}_S{:d}K.p".format(graph_type, motif_size,
                                          sample_size/1000)

    with open(fpath, "wb") as pfile:
        pickle.dump(data, pfile)
    


    
    



    
