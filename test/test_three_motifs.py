

import unittest, os

import graph_tool as gt
import numpy as np

from comp.functions import ( sample_three_motifs,
                             generate_three_motif_list )


class Test_sample_three_motifs(unittest.TestCase):

    # g = gt.Graph()
    # g.add_vertex(5)
    # g.add_edge(g.vertex(0), g.vertex(1))
    # g.add_edge(g.vertex(1), g.vertex(2))
    # g.add_edge(g.vertex(2), g.vertex(0))

    # # print(gt.topology.isomorphism(g, g))
    # x = sample_three_motifs(g, 20)
    # # print( x )

    def test_single_matches_from_motif_list(self):
        three_motif_list = generate_three_motif_list(with_empty=True)
    
        for k,motif in enumerate(three_motif_list):
            matches = sample_three_motifs(motif,1)
            self.assertEqual(int(np.where(np.array(matches)==1)[0]),
                             k)



if __name__ == '__main__':
    unittest.main()



