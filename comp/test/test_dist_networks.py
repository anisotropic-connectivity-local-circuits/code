
import unittest, os
import numpy as np
import graph_tool as gt
import graph_tool.stats
import graph_tool.topology

# get tested
from functions import ( connect_dist_network,
                        generate_dist_network )

# functions assisting in testing
from functions import ( distribute_neurons_randomly,
                        Aniso_netw_dist_profile,
                        eval_connectivity )


class Test_connect_dist_network(unittest.TestCase):

    g = gt.Graph()
    N = 100
    ed_l = 100.
    
    positions = distribute_neurons_randomly(N, ed_l)     
    xy = g.new_vertex_property("vector<double>")
    for k in range(N):
        g.add_vertex()
        xy[g.vertex(k)] = list(positions[k])
    g.vertex_properties["xy"] = xy

    def test_all_to_all_connectivity(self):
        d = lambda x: 1.
        g = connect_dist_network(self.g, d)
        self.assertEqual(g.num_edges(), self.N*(self.N-1))
        self.g.clear_edges()
        
    def test_none_to_none_connectivity(self):
        d = lambda x: 0.
        g = connect_dist_network(self.g, d)
        self.assertEqual(g.num_edges(), 0)
        self.g.clear_edges()


class Test_generate_dist_network(unittest.TestCase):

    N, ed_l, w = 1000, 100, 12.6
    dist_profile = Aniso_netw_dist_profile(w)
    spath = 'data/test/N1000_dist.gt'

    g = generate_dist_network(N, dist_profile.C, ed_l,
                              save_path = spath)


    def test_number_of_vertices(self):
        self.assertEqual(self.N, self.g.num_vertices())

    # graph properties
    def test_graph_property_graph_type(self):
        self.assertEqual(self.g.graph_properties["graph_type"],
                         "dist_depend")
        
    def test_graph_property_edge_length(self):
        self.assertEqual(self.g.graph_properties["ed_l"],
                         self.ed_l)
    
    def test_graphy_property_rewired(self):
        self.assertFalse(self.g.graph_properties["rewired"])
        
    def test_graphy_property_self_loops(self):
        self.assertFalse(self.g.graph_properties["self_loops"])

    def test_graphy_property_parallel_edges(self):
        self.assertFalse(self.g.graph_properties["parallel_edges"])

        
    def test_vertex_property_xy(self):
        xy = self.g.vertex_properties["xy"]
        for i in [0,self.N-1]:
            self.assertEqual(type(xy[self.g.vertex(i)][0]), float)
            self.assertEqual(type(xy[self.g.vertex(i)][1]), float)
            self.assertGreaterEqual(xy[self.g.vertex(i)][0], 0.)
            self.assertGreaterEqual(xy[self.g.vertex(i)][1], 0.)
            self.assertLessEqual(xy[self.g.vertex(i)][0], 212.)
            self.assertLessEqual(xy[self.g.vertex(i)][1], 212.)

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
        mu = eval_connectivity(self.g)
        # match the expected connectivity mu=0.116 +- 0.01
        self.assertLess(0.096, mu)
        self.assertGreater(0.126, mu)   
    

if __name__ == '__main__':
    unittest.main()
