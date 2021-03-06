
import unittest, os

import numpy as np

import graph_tool as gt
import graph_tool.stats
import graph_tool.topology

# get tested
from comp.functions import ( generate_aniso_network,
                             rotate,
                             find_axon_targets )

# functions assisting in testing
from comp.functions import ( eval_connectivity )


class Test_rotate(unittest.TestCase):

    x = [[1,1], [0,0], [-5,5]]

    def test_correct_result(self):

        self.assertTrue(np.allclose(
            rotate(np.pi, self.x),
            np.array([[-1.,-1.],[0.,0.],[5.,-5.]])))


class Test_find_axon_targets(unittest.TestCase):

    positions = np.array([[0,0],[1,1],[-1,1],[-1,-1],[1,-1]])
    positions = positions + np.array([1,1])

    def test_find_correct_targets(self):
        w = lambda x: .5
        self.assertListEqual([],
            find_axon_targets(0, 0, self.positions, w))
        for k in [1,2,3,4]:         
            self.assertEqual([k],
                find_axon_targets(0, np.pi/4.+np.pi/2.*(k-1),
                                  self.positions, w))

        
class Test_generate_aniso_network(unittest.TestCase):

    # TODO:
    # 1. test vertex propoerty for assigned ed_l as well

    N = 1000
    w = lambda x: 12.6
    spath = 'data/tmp_N1000_w126.gt'
    ed_l = 100.
    g = generate_aniso_network(N, w, ed_l,
                               save_path=spath)

    w_t = lambda x: x
    g_t = generate_aniso_network(N, w_t, ed_l)
    
    def test_number_of_vertices(self):
        self.assertEqual(self.N, self.g.num_vertices())

    # graph properties
    def test_graph_property_graph_type(self):
        self.assertEqual(self.g.graph_properties["graph_type"],
                         "aniso")
        
    def test_graph_property_edge_length(self):
        self.assertEqual(self.g.graph_properties["ed_l"],
                         self.ed_l)
    
    def test_graphy_property_rewired(self):
        self.assertFalse(self.g.graph_properties["rewired"])
        
    def test_graphy_property_self_loops(self):
        self.assertFalse(self.g.graph_properties["self_loops"])

    def test_graphy_property_parallel_edges(self):
        self.assertFalse(self.g.graph_properties["parallel_edges"])

    # vertex properties
    def test_vertex_property_xy(self):
        xy = self.g.vertex_properties["xy"]
        for i in [0,self.N-1]:
            self.assertEqual(type(xy[self.g.vertex(i)][0]), float)
            self.assertEqual(type(xy[self.g.vertex(i)][1]), float)
            self.assertGreaterEqual(xy[self.g.vertex(i)][0], 0.)
            self.assertGreaterEqual(xy[self.g.vertex(i)][1], 0.)
            self.assertLessEqual(xy[self.g.vertex(i)][0], 212.)
            self.assertLessEqual(xy[self.g.vertex(i)][1], 212.)


    def test_vertex_property_alpha(self):
        alpha = self.g.vertex_properties["alpha"]
        for v in self.g.vertices():
            self.assertEqual(type(alpha[v]), float)
            self.assertGreaterEqual(alpha[v], 0.)
            self.assertLessEqual(alpha[v], 2*np.pi)

            
    # we expect the graph to have no self loops
    def test_graph_self_loops(self):
        ne_before = self.g.num_edges()
        gt.stats.remove_self_loops(self.g)
        ne_after = self.g.num_edges()
        self.assertEqual(ne_before, ne_after)

    # we expect the graph to have no parallel edges
    def test_graph_parallel_edges(self):
        ne_before = self.g.num_edges()
        gt.stats.remove_parallel_edges(self.g)
        ne_after = self.g.num_edges()
        self.assertEqual(ne_before, ne_after)


    def test_graph_saving(self):
        h = gt.load_graph(self.spath)
        self.assertTrue(gt.topology.isomorphism(self.g,h))
        os.remove(self.spath)
        
    def test_expected_connectivity(self):
        N, w, ed_l = 1000, lambda x: 12.6, 100.
        mu_list = []
        for k in range(3):
            h = generate_aniso_network(N, w, ed_l)        
            mu_list.append(eval_connectivity(h))
        mu = np.mean(mu_list)
        # expected 0.116 +- 0.05
        self.assertGreaterEqual(mu, 0.111)
        self.assertLessEqual(mu, 0.121)

    def test_axon_angle_distribution_has_mean_zero(self):
        alpha = self.g.vertex_properties["alpha"]
        dirs = [[np.sin(alpha[v]), np.cos(alpha[v])]
                for v in self.g.vertices()]
        norm = lambda x: np.sqrt(np.sum(x**2))
        self.assertLess(norm((np.mean(dirs,0))), 0.1)
            

    # tuned aniso graphs

    def test_tuned_graph_property(self):
        self.assertEqual(self.g_t.graph_properties["graph_type"],
                         "tuned_aniso")
        

if __name__ == '__main__':
    unittest.main()
