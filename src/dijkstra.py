import math
import heapq as hq
import pickle, dill
import numpy as np
import pickle
import math
import time 

def get_neighbours(graph, node):

    neighbours = []
    # for i in range(0,len(graph[node])):
    #   neighbours.append(graph[node][i][0])
    # return neighbours
    # print(graph[node])
    for i in graph[node]:
        # print(i)
        neighbours.append(i)
        # print(neighbours)
    return neighbours
    

def reconstruct_path(cameFrom, current_node):
    total_path = [current_node]
    while current_node in cameFrom:
        current_node = cameFrom[current_node]
        total_path.append(current_node)
    total_path.reverse()
    return total_path

def dijkstra(graph, start_node, goal_node):
    start_time = time.time()
    # For each node, the cost of going from start to that node
    gScore = {}

    # For each node, cost of going from start to that node plus 
    # heuristic cost estimate of going from that node to the goal
    fScore = {}

    # For each node, the node it can be most efficiently reached from
    cameFrom = {}
    
    # Set default values of fScore and gScore for all nodes to infinity
    for node in graph:
        fScore[node] = math.inf
        gScore[node] = math.inf
    
    # Cost of going from start to start is zero
    gScore[start_node] = 0

    # Estimated cost from start to goal is completely heuristic
    fScore[start_node] = 0
    
    # List of discovered but unevaluated nodes and their estimated total costs
    # Initially only start node is known
    openSet = {start_node: fScore[start_node]}

    # List of evaluated nodes
    closedSet = []
    iteration = 0
    while openSet:
        runtime = time.time() - start_time
        # Move to node with lowest estimated total cost
        current_node = min(openSet, key=openSet.get)
        print('\rIteration: %s, Runtime: %s' % (str(iteration), str(np.around(runtime, decimals=5))), end='', flush=True)
        iteration+=1
        if current_node == goal_node:
            return reconstruct_path(cameFrom, current_node), gScore[goal_node]

        # Move current node to closed set
        del openSet[current_node]
        closedSet.append(current_node)

        neighbours = get_neighbours(graph, current_node)

        for neighbour in neighbours:
            # Ignore neighbours that have already been evaluated
            if neighbour in closedSet:
                continue
                
            # Calculate distance from start to neighbour
            item_node = 0
            # print(graph[current_node])
            for item in graph[current_node]:
                if item == neighbour:
                    item_node = item
            prelim_gScore = gScore[current_node] + graph[current_node][item_node]
            

            if prelim_gScore >= gScore[neighbour]:
                # Not a better path
                continue

            # New best path
            cameFrom[neighbour] = current_node
            gScore[neighbour] = prelim_gScore
            fScore[neighbour] = gScore[neighbour]
            
            # Discover new node
            if neighbour not in openSet:
                openSet[neighbour] = fScore[neighbour]
    # print(fScore)
    # print(gScore)
    # print(cameFrom)
    return reconstruct_path(cameFrom, goal_node), gScore[goal_node]
