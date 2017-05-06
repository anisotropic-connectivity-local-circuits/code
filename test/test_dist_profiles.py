
import unittest
import numpy as np
import graph_tool as gt

# get tested
from comp.functions import ( Aniso_netw_dist_profile )

# functions assisting in testing
from comp.functions import ( generate_dist_network,
                             eval_connectivity )


class Test_Aniso_netw_dist_profile(unittest.TestCase):


    def test_expected_connectivity(self):
        an_ddcp = Aniso_netw_dist_profile(37.3)
        N, ed_l = 1000, 296
        mu_list = []
        for k in range(3):
            h = generate_dist_network(N, an_ddcp.C, ed_l)        
            mu_list.append(eval_connectivity(h))
        mu = np.mean(mu_list)
        # expected 0.116 +- 0.05
        self.assertGreaterEqual(mu, 0.111)
        self.assertLessEqual(mu, 0.121)

   

if __name__ == '__main__':
    unittest.main()

