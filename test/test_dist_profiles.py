
import unittest
import numpy as np
import graph_tool as gt
import graph_tool.stats

# get tested
from comp.functions import ( Aniso_netw_dist_profile,
                             Tuned_netw_dist_profile )

# functions assisting in testing
from comp.functions import ( generate_dist_network,
                             generate_aniso_network,
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


class Test_Tuned_netw_dist_profile(unittest.TestCase):

    def test_expected_connectivity(self):
        tn_ddcp = Tuned_netw_dist_profile()
        N, ed_l = 1000, 296
        mu_list = []
        for k in range(3):
            h = generate_aniso_network(N, tn_ddcp.C, ed_l)        
            mu_list.append(eval_connectivity(h))
        mu = np.mean(mu_list)
        # expected 0.116 +- 0.05
        self.assertGreaterEqual(mu, 0.111)
        self.assertLessEqual(mu, 0.121)


    def test_graph_self_loops(self):
        tn_ddcp = Tuned_netw_dist_profile()
        N, ed_l = 1000, 296
        g = generate_aniso_network(N, tn_ddcp.C, ed_l)        
        ne_before = g.num_edges()
        gt.stats.remove_self_loops(g)
        ne_after = g.num_edges()
        self.assertEqual(ne_before, ne_after)

    
if __name__ == '__main__':
    unittest.main()

