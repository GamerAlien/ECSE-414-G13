from functools import reduce
from math import sqrt
from random import choice
from random import random
from time import time as time

import dill
import networkx as nx
import numpy as np
import sys

#Creates an entire network of the specified size
def create(size, randomness):

    start_time = time()

    num_as = int(sqrt(size))

    as_boundaries = list(np.unique(np.random.randint(1, size, num_as)))
    as_boundaries.insert(0,0)
    as_boundaries.append(size)

    #Greate an autonomous system (a.k.a a sub network)
    def create_as(start, end): 

        print('Generating AS with nodes ' + str(start) + ' to ' + str(end-1) + '...')

        m = randomness

        # select some edge destinations
        L = np.random.choice(range(start, end), 2*m)
        # and suppose that each edge has a weight
        weights = 0.5 + 5 * np.random.rand(m)

        # create a graph object, add nodes to it, and the edges
        G = nx.DiGraph()
        G.add_nodes_from(range(start, end))
        for i, (fr, to) in enumerate(zip(L[1::2], L[::2])):
            if fr != to:
                G.add_edge(fr, to, weight=np.around(weights[i])+1)
        return G

    as_list = list(map((lambda x : create_as(x[0], x[1])), zip(as_boundaries, as_boundaries[1:])))

    print('Generating AS topology...')
    as_topology = nx.random_tree(len(as_list))

    print('Connecting AS...')
    network = reduce((lambda x, y : nx.compose(x,y)), as_list)

    msp = {}
    get_as = {}
    edge_node = {}
    next_as = {}
    

    for as_id in range(len(as_list)):
        edge_node[as_id] = {}
        next_as[as_id] = {}

    for as1_id in range(len(as_list)):

        as1 = as_list[as1_id]

        for node in list(as1.nodes().keys()):
            get_as[node] = as1_id

        for as2_id in as_topology[as1_id]:

            as2 = as_list[as2_id]

            #Choose a node from first AS
            as1_edge_node = choice(list(as1.nodes().keys()))

            #Choose a node from first AS
            as2_edge_node = choice(list(as2.nodes().keys()))

            #Generate a random weight
            network.add_edge(as1_edge_node, as2_edge_node, weight=0.5 + 5 * random())

            msp[as1_edge_node] = nx.shortest_path(as1,source=as1_edge_node)
            edge_node[as1_id][as2_id] = as1_edge_node
            edge_node[as2_id][as1_id] = as2_edge_node

        for as2_id in range(len(as_list))[as1_id+1:]:

            as1_to_as2_path = nx.shortest_path(as_topology, as1_id, as2_id)
            next_as[as1_id][as2_id] = as1_to_as2_path[1]
            next_as[as2_id][as1_id] = as1_to_as2_path[-2]

    def heuristic(node1, node2):
        as1 = get_as[node1]
        as2 = get_as[node2]
        if as1 != as2:
            return msp[edge_node[as1][next_as[as1][as2]]][node1] + msp[edge_node[as2][next_as[as2][as1]]][node2]
        else:
            return 0

    runtime = time() - start_time
    print("Graph generated in "+str(np.around(runtime, decimals=5))+" seconds!")

   #Open output file
    outfile = open(str(size) + '.network' ,'wb')

    #Write network and heuristics to output file
    dill.dump({'network' : network, 'heuristic' : heuristic}, outfile)

    #Close output file
    outfile.close()

def load(size):
    infile = open(str(size) + '.network' ,'rb')
    network = dill.load(infile)
    infile.close()
    return network

"""
TODO make it not crash at this test
create(20000, 30)
net = load(20000)
h = net['heuristic']
print(h(0, 15))
print(h(550, 3500))
print(h(0, 19999))
"""
