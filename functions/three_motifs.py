# -*- coding: utf-8 -*-

import graph_tool as gt
import graph_tool.stats
import graph_tool.topology

import numpy as np


def generate_three_motif_list(with_empty):
    '''
    Does not contain first motif without edges!
    '''

    graph_list = []

    if with_empty:

        #      o
        #   ↙↗ ↘↖  
        #  o   ⇄  o
        g = gt.Graph()
        g.add_vertex(3)
        graph_list.append(g)

    #      o
    #   ↙↗ ↘↖  
    #  o   ⇄  o
    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(0),g.vertex(2))
    graph_list.append(g)


    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(2),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(2))
    g.add_edge(g.vertex(1),g.vertex(2))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(2))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(2),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(1))
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(0),g.vertex(2))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(2),g.vertex(1))
    g.add_edge(g.vertex(0),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(0))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(1))
    g.add_edge(g.vertex(2),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(0),g.vertex(2))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(0),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(1),g.vertex(0))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(1))
    graph_list.append(g)

    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(2),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(0),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(0),g.vertex(1))
    graph_list.append(g)

    # g = gt.Graph()
    # g.add_vertex(3)
    # g.add_vertex(3)
    g = gt.Graph()
    g.add_vertex(3)
    g.add_edge(g.vertex(0),g.vertex(1))
    g.add_edge(g.vertex(1),g.vertex(0))
    g.add_edge(g.vertex(2),g.vertex(0))
    g.add_edge(g.vertex(0),g.vertex(2))
    g.add_edge(g.vertex(1),g.vertex(2))
    g.add_edge(g.vertex(2),g.vertex(1))
    graph_list.append(g)

    return graph_list



def sample_three_motifs(g, sampling_size):

    ''' 
    Also return counts for motifs 0,1 and 2, 
    however only small sampling size viable due to long runtimes.
    '''

    # assert that g contains need self-loops nor parallel edges
    ne_before = g.num_edges()
    gt.stats.remove_self_loops(g)
    gt.stats.remove_parallel_edges(g)
    ne_after = g.num_edges()
    assert(ne_before == ne_after)

    three_motif_list = generate_three_motif_list(with_empty=False)
    motif_counts = np.zeros(len(three_motif_list)+1)    
    
    N = g.num_vertices()

    for k in range(sampling_size):

        vertex_ids = np.array([])
        while len(np.unique(vertex_ids)) < 3:
            vertex_ids = np.random.randint(0,N,3)

        is_part_of_motif = g.new_vertex_property("bool")
              
        for v_id in vertex_ids:
            is_part_of_motif[g.vertex(v_id)] = True

        g.set_vertex_filter(is_part_of_motif)

        motif_matches = []

        # test for motif without edges separately as 
        # graph_tool.topology does not handle it
        if g.num_edges()==0:
            motif_matches = [1]+[0]*len(three_motif_list)                            
        else:
            motif_matches.append(0)
          
            for motif in three_motif_list:
                if gt.topology.isomorphism(g,motif):
                    motif_matches.append(1)
                else:
                    motif_matches.append(0)
    
        if sum(motif_matches) == 0:
            print "Error, no matching motif found."    
            
        elif sum(motif_matches) > 1:
            print "Error, more than 1 motif match."
        
        motif_counts += np.array(motif_matches)

        g.set_vertex_filter(None)

    # b = time.time()

    # print "Finished at ", datetime.datetime.now(), ","
    # print "Runtime: ", (b-a)/sampling_size

    return list(motif_counts)

