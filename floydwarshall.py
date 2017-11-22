import texttable_mod
import graph_generator
import math
import time
import numpy as np
import pickle
import network
import sys



#Creates the adjacency matrixes for distance and predecessors
def createAdjacencyMatrix(graph, dist, pred):
    # print("Creating adjacency matrix...")
    for u in graph:
        #initialize the row
        # print("u "+ str(graph[u]))
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            #initialize all distances to infinity
            # print(v)
            dist[u][v] = math.inf
            #initialize all predecessors to infinity
            pred[u][v] = -1
        #distance from u to u is 0
        dist[u][u] = 0
        #fill matrix with every nodes' immediate neighbors weights (if possible)
        for neighbor in graph[u]:
            # print("neighbor: "+str(neighbor[1]))
            dist[u][neighbor[0]] = neighbor[1]
            pred[u][neighbor[0]] = u

def floydwarshall(graph):
    start_time = time.time()
    #source: https://jlmedina123.wordpress.com/2014/05/17/floyd-warshall-algorithm-in-python/
 
    # Initialize dist and pred:
    dist = {}
    pred = {}
    # Create Adjacency Matrix   
    createAdjacencyMatrix(graph, dist, pred)
    # print("Created Adjacency matrix!")
    # print("Started algorithm...")
    for t in graph:
        # given dist u to v, check if path u - t - v is shorter
        runtime = time.time() - start_time
        print('\rLoop: %s, Runtime: %s' % (str(t), str(np.around(runtime, decimals=5))), end='', flush=True)
        # print("Loop: "+str(t)+", Runtime: "+)
        for u in graph:
            for v in graph:
                # if any distances are infinity, then set new dist to infinity
                if(dist[u][t] == "inf" or dist[t][v] == "inf"):
                    newdist = "inf"
                else:
                    newdist = dist[u][t] + dist[t][v]
                #check if the new computed path from u to v through t is shorter than the path from u to v previously computed
                if newdist != "inf":
                    if newdist < dist[u][v]:
                        dist[u][v] = newdist
                        pred[u][v] = pred[t][v] # route new path through t
    return dist, pred

#gets the shortest path's cost and nodes
def getShortestPath(dist, pred, start, finish):
    # print('Cost:          ' + str(dist[start][finish]))
    finished = False;
    predecesor = finish

    path = "->"+str(finish)

    while not finished:

        predecesor = pred[start][predecesor]
        if predecesor == -1:
            path = str(start)+path
            break

        if predecesor == start:
            path = str(start)+path
            break
        path = "->"+str(predecesor)+path
    # print('Optimal path:  ' + str(path))
    return {'path': str(path), 'cost': str(dist[start][finish])}

#main algorithm method
def getFloydWarshallResults(graph, start, end):
    start_time = time.time()
    dist, pred = floydwarshall(graph);
    delay = 0.1
    time.sleep(delay)
    runtime = time.time() - start_time - delay
    # print("Done!")

    results = getShortestPath(dist, pred, start, end)
    # print('Runtime:       ' + str(np.around(runtime, decimals=5))+ " seconds\n")
    return{'runtime': str(np.around(runtime, decimals=5)), 'cost': results['cost'], 'path': results['path']}
	#will print the matrixes only if < 10 nodes
    # if(len(dist) <= 10):
        # print("Shortest distance matrix from each vertex:\n")
        # printMatrix(dist.copy());
        # print("\nPredecesors matrix in shortest path:\n")
        # printMatrix(pred.copy(), False);

    
    
#Helper function
#Prints matrixes using texttable_mod from texttable
#Will format distance to a->b:c if set
def printMatrix(matrix, distance=True):
    array_index = {}
    array_index[0] = "/"
    for i,x in enumerate(matrix):
        array_index[i+1] = x

    table = texttable_mod.Texttable()
    table.header(array_index)
    display_matrix = {}
    for i,x in enumerate(matrix):
        display_matrix[i] ={}
        display_matrix[i][0]=x
        for j,y in enumerate(matrix):
            if matrix[x][y] != math.inf:
                if(distance):
                    display_matrix[i][j+1] = str(x)+"->"+str(y)+" : "+str(matrix[x][y])
                else:
                    display_matrix[i][j+1] = matrix[x][y]
            else:
                display_matrix[i][j+1] = "inf"
    table.add_rows(display_matrix, False)
    print(table.draw())
    

def main():
    # # G = generateGraph(100, 100)

    # G = graph_generator.generateERGraph(1000, 0.15, 1, 12)
   
    # print("Number of edges: " + str(G.number_of_edges()))    
    
    
    # graph = graph_generator.getFormattedGraph(G)
    # print("Graph Formatted!")
    
    # getFloydWarshallResults(graph)
    # graph_generator.drawGraph(G)
    

    #Generate network
    NET_SIZE = 10

    netData = network.create(NET_SIZE)

    #Generate all heuristics
    heuristics = {}
    #heuristics['heuristic A'] = heuristic.A(netData)

    #Open output file
    outfile = open("graph.pickle",'wb')

    #Write network and heuristics to output file
    pickle.dump(netData['network'],outfile)
    outfile.close()

    graph = pickle.load(open( "graph.pickle", "rb" ))
    # print(graph)
    getFloydWarshallResults(graph, 0, 9)


 

if __name__ == '__main__':
    main()