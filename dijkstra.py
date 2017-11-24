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
    # set distance of source to zero (takes nothing to get to the source node)
    distance[source_node] = 0
    # iterative initialization for each vertex in graph
    for vertex in graph:
        if vertex != source_node:
            # set all distance to infinity initially
            distance[vertex] = math.inf
            # set all nodes to have no predecessor initially
            previous_node[vertex] = None
            # push vertex to heap
            hq.heappush(unvisited, (distance[vertex], vertex))
    # finally, push the source node to the stack
    hq.heappush(unvisited, (distance[source_node], source_node))
    while unvisited:
        # pop node with least distance from the heap
        closest_node = hq.heappop(unvisited)[1]
        for neighbour in graph[closest_node]:
            # compute distance to neightbour through closest node
            new_distance = distance[closest_node] + graph[closest_node][neighbour]
            if new_distance < distance[neighbour]:
                # find the neighbour in the heap
                neighbour_index = unvisited.index((distance[neighbour], neighbour))
                # set new distance as the new closest distance to neighbour
                distance[neighbour] = new_distance
                # now the predecessor is closest_node
                previous_node[neighbour] = closest_node
                # set the new distance on the tuple stored in heap

                ##uncomment for linear method
                unvisited[neighbour_index] = (new_distance, neighbour)

                #uncomment for heap method
                #new_node = (new_distance, neighbour)

                # siftup the newly adjusted node until properly placed to preserve heap invariance

                ## essentially linear method
                # hq._siftup(unvisited, neighbour_index)
                hq.heapify(unvisited)

                ## heap method
                #unvisited.pop(neighbour_index)
                #hq.heappush(unvisited, new_node)
                #print(unvisited)
    return distance

def targetted_dijkstra(graph, source_node,destination):
    # initialize distance dict
    distance = {}
    # initialize previous node dict
    previous_node = {}
    # initialize unvisited list
    unvisited = []
    # set distance of source to zero (takes nothing to get to the source node)
    distance[source_node] = 0
    # iterative initialization for each vertex in graph
    for vertex in graph:
        if vertex != source_node:
            # set all distance to infinity initially
            distance[vertex] = math.inf
            # set all nodes to have no predecessor initially
            previous_node[vertex] = None
            # push vertex to heap
            hq.heappush(unvisited, (distance[vertex], vertex))
    # finally, push the source node to the stack
    hq.heappush(unvisited, (distance[source_node], source_node))
    while unvisited:
        # pop node with least distance from the heap
        closest_node = hq.heappop(unvisited)[1]
        for neighbour in graph[closest_node]:
            # compute distance to neightbour through closest node
            new_distance = distance[closest_node] + graph[closest_node][neighbour]
            if new_distance < distance[neighbour]:
                # find the neighbour in the heap
                neighbour_index = unvisited.index((distance[neighbour], neighbour))
                # set new distance as the new closest distance to neighbour
                distance[neighbour] = new_distance
                # now the predecessor is closest_node
                previous_node[neighbour] = closest_node
                # set the new distance on the tuple stored in heap
                # unvisited[neighbour_index] = (new_distance, neighbour)
                new_node = (new_distance, neighbour)
                # siftup the newly adjusted node until properly placed to preserve heap invariance
                # hq._siftup(unvisited, neighbour_index)
                # hq.heapify(unvisited)
                unvisited.pop(neighbour_index)
                hq.heappush(unvisited, new_node)
    return distance