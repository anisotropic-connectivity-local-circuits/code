
import unittest

import numpy as np

import graph_tool as gt
import graph_tool.stats 

from comp.functions import ( distribute_neurons_randomly,
                             connect_graph )


class Test_distribute_neurons_randomly(unittest.TestCase):

    N = 1000
    ed_l = 212
    pos = distribute_neurons_randomly(N, ed_l)

    def test_positions_are_within_square(self):
        self.assertLessEqual(np.max(self.pos), self.ed_l)
        self.assertGreaterEqual(np.min(self.pos), 0)

    def test_dimensions(self):
        self.assertTupleEqual(np.shape(self.pos), (self.N, 2))
        

class Test_connect_graph(unittest.TestCase):

    g = gt.Graph()
    g.add_vertex(5)

    def test_connection_established(self):
        g = connect_graph(self.g, 2, [1,4])
        targets = []
        for e in g.edges():
            self.assertEqual(int(e.source()), 2)
            targets.append(int(e.target()))
        self.assertListEqual(targets,[1,4])
        
        

if __name__ == '__main__':
    unittest.main()
