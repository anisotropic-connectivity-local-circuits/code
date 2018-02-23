

import unittest, os

import graph_tool as gt

from comp.functions import ( sample_three_motifs )


class Test_sample_three_motifs(unittest.TestCase):

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0), g.vertex(1))
    g.add_edge(g.vertex(1), g.vertex(2))
    g.add_edge(g.vertex(2), g.vertex(0))

    sample_three_motifs(g, 10)


if __name__ == '__main__':
    unittest.main()



