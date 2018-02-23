

import unittest, os

import graph_tool as gt
import numpy as np

from comp.functions import ( sample_three_motifs,
                             generate_three_motif_list )


class Test_sample_three_motifs(unittest.TestCase):

    
    def test_single_matches_from_motif_list(self):
        three_motif_list = generate_three_motif_list(with_empty=True)
    
        for k,motif in enumerate(three_motif_list):
            matches = sample_three_motifs(motif,1)
            self.assertEqual(int(np.where(np.array(matches)==1)[0]),
                             k)

    def test_empty_graph(self):
        g = gt.Graph()
        g.add_vertex(100)

        matches = sample_three_motifs(g,50)
        self.assertEqual(matches[0],50)
        

    def test_fully_connected_graph(self):
        g = gt.Graph()
        n = 100
        g.add_vertex(n)
        for i in range(n):
            for j in range(n):
                if i!=j:
                    g.add_edge(g.vertex(i), g.vertex(j))

        matches = sample_three_motifs(g,50)
        self.assertEqual(matches[-1],50)
        


if __name__ == '__main__':
    unittest.main()



