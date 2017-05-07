
from functions import eval_connectivity
import graph_tool as gt
import numpy as np
import scipy.stats, sys

P = []
for gpath in sys.argv[1:]:
    g = gt.load_graph(gpath)
    P.append(eval_connectivity(g))

assert(len(P) == 5)
    
print "Overall connection probability:"
print "\t", np.mean(P), " +-", scipy.stats.sem(P)
    



    
