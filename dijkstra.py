import math
import heapq as hq
import graph_generator

def dijkstra(graph, source_node):
    # initialize distance dict
    distance = {}
    # initialize previous node dict
    previous_node = {}
    # initialize unvisited list
    unvisited = []
    # iterative initialization for each vertex in graph
    for vertex in graph:
        if vertex != source_node:
            # set all distance to infinity initially
            distance[vertex] = math.inf
            # set all nodes to have no predecessor initially
            previous_node[vertex] = None
            # push vertex to heap
            hq.heappush(unvisited, (distance[vertex], vertex))

    while unvisited:
        # pop node with least distance from the heap
        closest_node = hq.heappop(unvisited)
        for neighbour in graph[closest_node]:
            # compute distance to neightbour through closest node
            new_distance = distance[closest_node] + neighbour[1]
            if new_distance < distance[neighbour]:
                # set new distance as the new closest distance to neighbour
                distance[neighbour] = new_distance
                # now the predecessor is closest_node
                previous_node[neighbour] = closest_node
                # find the neighbour in the heap
                neighbour_index = unvisited.index(neighbour)
                # set the new distance on the tuple stored in heap
                unvisited[neighbour_index][0] = new_distance
                # siftup the newly adjusted node until properly placed to preserve heap invariance
                hq._siftup(unvisited, neighbour_index)
    return distance

G = graph_generator.generateERGraph(10, 0.15, 1, 10)
graph = graph_generator.getFormattedGraph(G)
dijkstra(graph,0)