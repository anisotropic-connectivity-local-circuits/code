
import unittest

import numpy as np

import graph_tool as gt

from functions import eval_connectivity 


class Test_eval_connectivity(unittest.TestCase):

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0), g.vertex(1))
    g.add_edge(g.vertex(1), g.vertex(2))
    g.add_edge(g.vertex(2), g.vertex(0))

    def test_correct_connectivity(self):
        self.assertEqual(eval_connectivity(self.g),
                         0.5)       

if __name__ == '__main__':
    unittest.main()
