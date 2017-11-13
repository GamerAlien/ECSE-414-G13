import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import time

# using networkx, manually generate a random undirected weighted graph
def generateGraph(nodes, randomness):
    print("Generating graph...")
    n = nodes; m = randomness

    # select some edge destinations
    L = np.random.choice(range(n), 2*m)
    # and suppose that each edge has a weight
    weights = 0.5 + 5 * np.random.rand(m)

    # create a graph object, add n nodes to it, and the edges
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for i, (fr, to) in enumerate(zip(L[1::2], L[::2])):
        if fr != to:
            G.add_edge(fr, to, weight=np.around(weights[i])+1)
    print("Graph generated!")
    return G

#used in conjunction with generateERGraph()
#Sets random weights to existing edges
def setEdgeWeights(G, range_start, range_end):
    print("Setting random weights between "+str(range_start)+" and "+str(range_end)+" to all edges...")
    for u, d in G.nodes(data=True):
        for n in G.neighbors(u):
            G[u][n]['weight'] = random.randrange(range_start, range_end)
    return G

# using networkx library, generate a random undirected unweighted graph
def generateERGraph(nodes, edge_probability, range_start, range_end):
    start_time = time.time()
    print("Generating weightless graph with "+str(nodes)+" nodes and an edge probability of "+str(edge_probability)+"...")
    G = nx.erdos_renyi_graph(nodes,edge_probability)
    print("Generated graph!")
    G = setEdgeWeights(G, range_start, range_end)
    print("Edge weights set!")
    runtime = time.time() - start_time
    print("Graph generated in "+str(np.around(runtime, decimals=5))+" seconds!")
    return G
    
#plots the graph
def drawGraph(G):
    nx.draw(G,with_labels=True)   
    plt.show()

#Formats the graph, to be of this format:
# graph = {
# 'A':[('B',2),('E',10)], 
# 'B':[('A',2),('C',5),('E',7)], 
# 'C':[('B',5),('D',2)], 
# 'D':[('C',2),('F',1)], 
# 'E':[('A',10),('B',7),('D',2),('F',3)], 
# 'F':[('D',1),('E',3)]}

def getFormattedGraph(G):
    print("Formatting graph...")
    formatted = {}
    for u,d in G.nodes(data=True):
        formatted[u] = {}
        # print("Node"+str(u))
        for n in G.neighbors(u):
            formatted[u][n] = int(G[u][n]['weight'])
    return formatted