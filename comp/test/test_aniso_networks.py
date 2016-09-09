
import unittest

import numpy as np

import graph_tool as gt
import graph_tool.stats 


from functions import distribute_neurons_randomly, generate_aniso_network


class Test_distribute_neurons_randomly(unittest.TestCase):

    N = 1000
    ed_l = 212
    pos = distribute_neurons_randomly(N, ed_l)

    def test_positions_are_within_square(self):
        self.assertLessEqual(np.max(self.pos), self.ed_l)
        self.assertGreaterEqual(np.min(self.pos), 0)

    def test_dimensions(self):
        self.assertTupleEqual(np.shape(self.pos), (self.N, 2))
        
        
class Test_generate_aniso_network(unittest.TestCase):

    # TODO:
    # 1. test vertex propoerty for assigned ed_l as well

    N = 1000
    w = 12.6
    g = generate_aniso_network(N, w)

    def test_number_of_vertices(self):
        self.assertEqual(self.N, self.g.num_vertices())

    # graph properties
    def test_graph_property_graph_type(self):
        self.assertEqual(self.g.graph_properties["graph_type"],
                         "anisotropic")
        
    def test_graph_property_edge_length(self):
        self.assertEqual(self.g.graph_properties["ed_l"],
                         212.)
    
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

              
    # def test_vertex_positions(self):
    #     self.


    # we expect the graph to have no self loops
    def test_graph_self_loops(self):
        ne_before = self.g.num_edges()
        gt.stats.remove_self_loops(self.g)
        ne_after = self.g.num_edges()
        self.assertEqual(ne_before, ne_after)

    # we expect the graph to have no self loops
    def test_graph_parallel_edges(self):
        ne_before = self.g.num_edges()
        gt.stats.remove_parallel_edges(self.g)
        ne_after = self.g.num_edges()
        self.assertEqual(ne_before, ne_after)
        

if __name__ == '__main__':
    unittest.main()
