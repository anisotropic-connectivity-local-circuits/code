
from params.sample_nmotif_ecounts_params import *

label = "nmotif_ecounts_{:s}_n{:d}_S{:d}K".format(graph_type, motif_size,
                                                  sample_size/1000)

if __name__ == "__main__":
    print label

