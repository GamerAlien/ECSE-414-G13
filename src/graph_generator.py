import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import pickle
import sys
import getopt
import os

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
    print("Number of edges: "+ str(G.number_of_edges()))
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
# 'F':[('D',1),('E',3)]}s
def getFormattedGraph(G):
    print("Formatting graph...")
    start_time = time.time()
    formatted = {}
    for u,d in G.nodes(data=True):
        print('\rLoop: %s, Runtime: %s' % (str(u), str(np.around(time.time() - start_time, decimals=5))), end='', flush=True)
        formatted[u] = {}
        # print("Node"+str(u))
        for n in G.neighbors(u):
            formatted[u][n] = int(G[u][n]['weight'])
    return formatted

def getFileName(size, percent):
    if percent == 0.2:
        filename = "../graphs/graph_"+str(size)+"_nodes_networkx_20percent.pickle"
    elif percent == 0.5:
        filename = "../graphs/graph_"+str(size)+"_nodes_networkx.pickle"
    else:
        filename = "../graphs/graph_"+str(size)+"_nodes_networkx_"+str(int(percent*100))+"percent.pickle"
    return filename

def createGraph(size, percent):

    print("--------------------- "+str(size)+" nodes ---------------------")
    start_time = time.time()
    G = generateERGraph(size, percent, 5, 50)
    graph = getFormattedGraph(G)
    runtime = time.time() - start_time
    outfile = open(getFileName(size, percent),'wb')
    pickle.dump(graph,outfile)
    outfile.close()
    print("\nRuntime: "+str(np.around(runtime, decimals=5)))
    return G

def main(argv):

    # ain(argv)
    if not os.path.exists("../graphs/"):
        print("Created graph directory!")
        os.mkdir("../graphs/")
    optlist, argv = getopt.getopt(argv, 'p:n:da', ['probability=', 'nodes='])


    percent = 0.20
    run_all=False
    draw = False
    nodes = 10
    for opt, arg in optlist:
        if opt in ('-p', '--probability'):
            try:
                if float(arg) < 0 or float(arg) > 1:
                    print("ERROR: probability not valid: use 0.2, 0.5...")
                    sys.exit(2)
                percent = float(arg)
            except:
                print("ERROR: Invalid probability!")
                sys.exit(2)
        elif opt in ('-n', '--nodes'):
            nodes = arg
        elif opt == '-a':
            run_all = True
        elif opt == '-d':
            draw = True

    if run_all:
        createGraph(10, percent)
        createGraph(100, percent)
        createGraph(500, percent)
        createGraph(1000, percent)
        createGraph(2000, percent)
        createGraph(5000, percent)
        createGraph(10000, percent)
        # createGraph(15000, percent)
        # createGraph(20000, percent)
    else:
        if draw:
            G = createGraph(int(nodes), percent)
            drawGraph(G)
        else:
            createGraph(int(nodes), percent) 

if __name__ == '__main__':
    main(sys.argv[1:])