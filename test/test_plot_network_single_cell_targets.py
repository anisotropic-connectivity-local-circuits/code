
import unittest, os, filecmp

import graph_tool as gt

# get tested
from plots import ( plot_network_single_cell_targets )

# functions assisting in testing
from functions import ( generate_aniso_network )


class Test_plot_network_single_cell_targets(unittest.TestCase):

    N = 1000
    w = lambda x: 12.6
    ed_l = 100.
    g = generate_aniso_network(N, w, ed_l)

    def test_generates_output_file(self):
        save_path = 'data/test/nsct_test.pdf'
        plot_network_single_cell_targets(self.g, 0, save_path)
        self.assertTrue(os.path.isfile(save_path))
        os.remove(save_path)

    def test_different_outputs_for_different_sources(self):
        s1 = 'data/test/nsct_test1.pdf'
        s2 = 'data/test/nsct_test2.pdf'
        plot_network_single_cell_targets(self.g, 1, s1)
        plot_network_single_cell_targets(self.g, 2, s2)
        self.assertFalse(filecmp.cmp(s1,s2))
        os.remove(s1)
        os.remove(s2)


if __name__ == '__main__':
    unittest.main()
