
import unittest

import numpy as np

import graph_tool as gt

# get tested
from functions import ( eval_connectivity,
                        get_xy,
                        get_target_ids )

# functions assisting in testing
from functions import ( generate_aniso_network )


class Test_eval_connectivity(unittest.TestCase):

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0), g.vertex(1))
    g.add_edge(g.vertex(1), g.vertex(2))
    g.add_edge(g.vertex(2), g.vertex(0))

    def test_correct_connectivity(self):
        self.assertEqual(eval_connectivity(self.g), 0.5)       


class Test_get_xy(unittest.TestCase):

    g = generate_aniso_network(50, lambda x: 1.,
                               ed_l = 100.)

    def test_number_of_xy_match(self):
        xs, ys = get_xy(self.g)
        self.assertEqual(len(xs), 50)
        self.assertEqual(len(ys), 50)

    def test_xy_in_correct_range(self):
        xs, ys = get_xy(self.g)
        for x in xs:
            self.assertGreaterEqual(x, 0.)
            self.assertLess(x, 100.)
        for y in ys:
            self.assertGreaterEqual(y, 0.)
            self.assertLess(y, 100.)


#class Test_get_target_ids(unittest.TestCase):
    
        
if __name__ == '__main__':
    unittest.main()
