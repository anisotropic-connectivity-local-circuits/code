
import unittest, os
import numpy as np

import graph_tool as gt
import graph_tool.topology

# get tested
from comp.functions import ( rewire )

# functions assisting in testing
from comp.functions import ( generate_aniso_network )


        
class Test_rewire(unittest.TestCase):

    g = gt.Graph()
    ed_l = 100
    
    edge_length = g.new_graph_property("double")
    edge_length[g] = ed_l
    g.graph_properties["ed_l"] = edge_length

    xy = g.new_vertex_property("vector<double>")
    g.vertex_properties["xy"] = xy

    def test_single_target_results_in_isomorphic_graph(self):
        # construct with a single edge that cannot be rewired
        h = gt.Graph(self.g)
        h.add_vertex(2)
        h.add_edge(h.vertex(0), h.vertex(1))
        xy = h.vertex_properties["xy"]
        xy[h.vertex(0)] = (50,50)
        xy[h.vertex(1)] = (55,55)
        k, stat = rewire(h)
        self.assertTrue(gt.topology.isomorphism(h,k))

    def test_rew_fraction_zero_results_in_isomorphic_graph(self):
        h = generate_aniso_network(100, lambda x: 12.6, 100)
        k, stat = rewire(h, rew_frac=0)
        self.assertTrue(gt.topology.isomorphism(h,k))

    def test_only_possible_targets_get_rewired(self):
        h = gt.Graph(self.g)
        h.add_vertex(2)
        h.add_edge(h.vertex(0), h.vertex(1))
        xy = h.vertex_properties["xy"]
        xy[h.vertex(0)] = (50,50)
        xy[h.vertex(1)] = (55,55)
        k, stat = rewire(h)
        self.assertTrue(gt.topology.isomorphism(h,k))
        
    def test_after_rewiring_rew_property_is_true(self):
        h = gt.Graph(self.g)
        h, stat = rewire(h)
        self.assertEqual(h.graph_properties["rewired"],True)

    g_aniso = generate_aniso_network(1000, lambda x: 12.6, 100)
    # g_aniso = gt.Graph(g)
    # g_aniso.add_vertex(2)
    # g_aniso.add_edge(g_aniso.vertex(0), g_aniso.vertex(1))
    # g_aniso.add_edge(g_aniso.vertex(0), g_aniso.vertex(1))
        
    # we expect the graph to have no self loops
    def test_graph_self_loops(self):
        ne_before = self.g_aniso.num_edges()
        gt.stats.remove_self_loops(self.g_aniso)
        ne_after = self.g_aniso.num_edges()
        self.assertEqual(ne_before, ne_after)

    # we expect the graph to have no parallel edges
    def test_graph_parallel_edges(self):
        ne_before = self.g_aniso.num_edges()
        gt.stats.remove_parallel_edges(self.g_aniso)
        ne_after = self.g_aniso.num_edges()
        self.assertEqual(ne_before, ne_after)



if __name__ == '__main__':
    unittest.main()
