
import unittest, itertools
import numpy as np
import graph_tool as gt

# get tested
from comp.functions import ( eval_connectivity,
                             get_xy,
                             get_target_ids,
                             get_dist_matrix,
                             get_adjacency_matrix,
                             get_ddcp,
                             get_dd_recip_p,
                             get_dists_of_connected_pairs,
                             get_2neuron_p,
                             get_nmotif_ecounts,
                             get_common_neighbours,
                             get_pref_dir,
                             get_isotropy_measure )

# functions assisting in testing
from comp.functions import ( generate_aniso_network,
                             distribute_neurons_randomly)


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


class Test_get_target_ids(unittest.TestCase):

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0), g.vertex(1))
    g.add_edge(g.vertex(0), g.vertex(2))

    def test_get_correct_target_ids(self):
        targets_0 = get_target_ids(self.g, 0)
        targets_1 = get_target_ids(self.g, 1)
        self.assertListEqual(targets_0, [1,2])
        self.assertListEqual(targets_1, [])
    


class Test_get_dist_matrix(unittest.TestCase):

    g = gt.Graph()

    positions = [[0.,0.],[1.,1.]]
    xy = g.new_vertex_property("vector<double>")
    for k in range(len(positions)):
        g.add_vertex()
        xy[g.vertex(k)] = list(positions[k])
    g.vertex_properties["xy"] = xy

    def test_correct_distances(self):
        D = get_dist_matrix(self.g)
        self.assertEqual(D[0][1], D[1][0])
        self.assertEqual(D[0][1], np.sqrt(2))
        self.assertEqual(D[0][0], D[1][1])
        self.assertEqual(D[0][0], 0.)

    def test_dist_matrix_symmetric(self):
        D = get_dist_matrix(self.g)
        np.testing.assert_array_equal(D,D.transpose())

    def test_dist_matrix_diagonal_equals_zero(self):
        D = get_dist_matrix(self.g)
        np.testing.assert_array_equal(np.diag(D),
                                      np.array([0.,0.]))



class Test_get_adjacency_matrix(unittest.TestCase):

    def test_empty_graph_has_zero_adjacency_matrix(self):
        g, N = gt.Graph(), 10
        g.add_vertex(N)
        np.testing.assert_array_equal(np.zeros((N,N)),
                                      get_adjacency_matrix(g))

    def test_fully_connected_graph_has_1_adjacency_matrix(self):
        g, N = gt.Graph(), 10
        g.add_vertex(N)
        for i,j in itertools.product(range(N), range(N)):
            g.add_edge(i,j)
        np.testing.assert_array_equal(np.ones((N,N)),
                                      get_adjacency_matrix(g))

    def test_specific_graph_for_adjacency_matrix(self):
        g = gt.Graph()
        g.add_vertex(4)
        g.add_edge_list([(1,2), (2,3), (3,2), (0,3)])

        expected_A = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 0, 1],
                               [1, 0, 1, 0]])

        np.testing.assert_array_equal(expected_A,
                                      get_adjacency_matrix(g))


class Test_get_ddcp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        N = 500
        g = gt.Graph()
        g.add_vertex(N)
        for i in range(N):
            for j in range(N):
                if not i==j:
                    g.add_edge(g.vertex(i),g.vertex(j))

        ed_l = 1
        positions = distribute_neurons_randomly(N, ed_l)     
        xy = g.new_vertex_property("vector<double>")
        for k in range(N):
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy
        self.g = g

    
    def test_fully_connected_net_returns_constant_1_probability(self):
        bins = np.linspace(0,1,num=10)
        np.testing.assert_array_equal(get_ddcp(self.g, bins)[1],
                                      np.ones(len(bins)-1))
        


class Test_get_dd_recip_p(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        N = 500
        g = gt.Graph()
        g.add_vertex(N)
        for i,j in itertools.product(range(N),range(N)):
            if not i==j:
                g.add_edge(g.vertex(i),g.vertex(j))

        ed_l = 1
        positions = distribute_neurons_randomly(N, ed_l)     
        xy = g.new_vertex_property("vector<double>")
        for k in range(N):
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy
        self.g = g

    
    def test_fully_connected_net_returns_constant_1_probability(self):
        bins = np.linspace(0,1,num=10)
        np.testing.assert_array_equal(get_dd_recip_p(self.g, bins)[1],
                                      np.ones(len(bins)-1))

    
class Test_get_dists_of_connected_pairs(unittest.TestCase):

    def _construct_graph(self):
        g = gt.Graph()
        positions = [[0.,0.],[1.,1.]]
        xy = g.new_vertex_property("vector<double>")
        for k in range(len(positions)):
            g.add_vertex()
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy
        return g
    
    def test_unconnected_graph_no_connected_pairs(self):
        g = self._construct_graph()
        D = get_dists_of_connected_pairs(g)
        self.assertEqual(len(D),0)

    def test_get_correct_distance(self):
        g = self._construct_graph()
        g.add_edge(0,1)
        D = get_dists_of_connected_pairs(g)
        self.assertEqual(len(D),1)
        self.assertEqual(D[0], np.sqrt(2))


class Test_get_2neuron_p(unittest.TestCase):

    def test_unconnected_graph(self):
        g = gt.Graph()
        g.add_vertex(5)
        self.assertEqual(get_2neuron_p(g), (1.,0.,0.))

    def test_ring_graph(self):
        g = gt.Graph()
        g.add_vertex(3)
        g.add_edge(g.vertex(0), g.vertex(1))
        g.add_edge(g.vertex(1), g.vertex(2))
        g.add_edge(g.vertex(2), g.vertex(0))
        self.assertEqual(get_2neuron_p(g), (0.,1.,0.))

    def test_all_to_all_graph(self):
        g = gt.Graph()
        g.add_vertex(3)
        g.add_edge(g.vertex(0), g.vertex(1))
        g.add_edge(g.vertex(1), g.vertex(2))
        g.add_edge(g.vertex(2), g.vertex(0))
        g.add_edge(g.vertex(0), g.vertex(2))
        g.add_edge(g.vertex(1), g.vertex(0))
        g.add_edge(g.vertex(2), g.vertex(1))
        self.assertEqual(get_2neuron_p(g), (0.,0.,1.))


class Test_get_nmotif_ecounts(unittest.TestCase):

    def test_empty_graph(self):
        g = gt.Graph()
        g.add_vertex(5)
        self.assertEqual(get_nmotif_ecounts(g,3,20), {0: 20})

    def test_all_to_all_graph(self):
        g = gt.Graph()
        g.add_vertex(30)
        for x,y in itertools.product(range(30), range(30)):
            if x != y:
                g.add_edge(g.vertex(x), g.vertex(y))
        self.assertEqual(get_nmotif_ecounts(g,8,15), {8*7: 15})

    def test_ring_graph(self):
        g = gt.Graph()
        g.add_vertex(3)
        g.add_edge(g.vertex(0), g.vertex(1))
        g.add_edge(g.vertex(1), g.vertex(2))
        g.add_edge(g.vertex(2), g.vertex(0))
        self.assertEqual(get_nmotif_ecounts(g,3,10), {3 : 10})



class Test_get_common_neighbours(unittest.TestCase):

    def test_empty_graph(self):
        g = gt.Graph()
        g.add_vertex(5)
        pairs, cn, in_nb, out_nb = get_common_neighbours(g)
        np.testing.assert_array_equal(cn, [0]*(5*4/2))
        np.testing.assert_array_equal(in_nb, [0.]*(5*4/2))
        np.testing.assert_array_equal(out_nb, [0.]*(5*4/2))

    def test_all_to_all_graph(self):
        g = gt.Graph()
        N = 15
        g.add_vertex(N)
        for x,y in itertools.product(range(N), range(N)):
            if x != y:
                g.add_edge(g.vertex(x), g.vertex(y))
    
        pairs, cn, in_nb, out_nb = get_common_neighbours(g)
        np.testing.assert_array_equal(cn, [2]*(N*(N-1)/2))
        np.testing.assert_array_equal(in_nb, [N-2.]*(N*(N-1)/2))
        np.testing.assert_array_equal(out_nb, [N-2.]*(N*(N-1)/2))


    def test_example_graph(self):
        # algorithm also counts self connections,
        # but not a problem here as used used 
        # graphs do not have self-loops
        g = gt.Graph()
        g.add_vertex(4)
        g.add_edge_list([(1,2), (2,3), (3,2), (0,3), (2,1),
                         (2,2), (1,1)])

        expected_A = np.array([[0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 1, 1],
                               [1, 0, 1, 0]])

        np.testing.assert_array_equal(expected_A,
                                      get_adjacency_matrix(g))

        expected_cn     = [0, 0, 1, 2, 0, 2]
        expected_out_nb = [0., 1., 0., 2., 1., 1.]
        expected_inn_nb = [0., 0., 0., 2., 1., 1.]

        pairs, cn, inn_nb, out_nb = get_common_neighbours(g)

        np.testing.assert_array_equal(expected_cn, cn)
        np.testing.assert_array_equal(expected_out_nb, out_nb)
        np.testing.assert_array_equal(expected_inn_nb, inn_nb)



class Test_get_pref_dir(unittest.TestCase):

    def test_docstring_example(self):
        np.testing.assert_array_almost_equal(
            get_pref_dir([[4,1],[7,-3],[5,1],[6,3]], 0),
            [ 0.76903559, -0.03096441], decimal=7)

        
class Test_get_isotropy_measure(unittest.TestCase):

    def test_empty_graph(self):
        g = gt.Graph()
        g.add_vertex(5)

        positions = [[0.,0.]]*5
        xy = g.new_vertex_property("vector<double>")
        for k in range(len(positions)):
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy

        np.testing.assert_array_equal(get_isotropy_measure(g), [])


    def test_evenly_spread_graph(self):
        g = gt.Graph()
        g.add_vertex(5)

        positions = [[0.,0.],[0.,1.],[1.,0.],[-1.,0.],[0.,-1]]
        xy = g.new_vertex_property("vector<double>")
        for k in range(len(positions)):
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy

        for i,j in itertools.product(range(5), range(5)):
            if i!=j:
                g.add_edge(i,j)

        np.testing.assert_array_equal(get_isotropy_measure(g)[0], [0.,0.])

    
    def test_evenly_spread_graph_different_lengths(self):
        g = gt.Graph()
        g.add_vertex(5)

        positions = [[0.,0.],[0.,1.],[1.,0.],[-5.,0.],[0.,-17]]
        xy = g.new_vertex_property("vector<double>")
        for k in range(len(positions)):
            xy[g.vertex(k)] = list(positions[k])
        g.vertex_properties["xy"] = xy

        for i,j in itertools.product(range(5), range(5)):
            if i!=j:
                g.add_edge(i,j)

        np.testing.assert_array_equal(get_isotropy_measure(g)[0], [0.,0.])


        
if __name__ == '__main__':
    unittest.main()


    
