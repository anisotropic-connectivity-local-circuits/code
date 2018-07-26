
from params.rewire_and_get_common_input_variance_params import *

label = 'cinpvar_{:s}_netw_nrews{:d}_efrac{:.2f}'.format(graph_type,
                                                           n_rew_stages,
                                                           eps_f)

if __name__ == "__main__":
    print label
