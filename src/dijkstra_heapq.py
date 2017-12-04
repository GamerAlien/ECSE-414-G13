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
                # siftup the newly adjusted node until properly placed to preserve heap invariance
                ## essentially linear method
                hq.heapify(unvisited)
                ## heap method
                # hq._siftdown(unvisited, 0, neighbour_index)
            print(unvisited)
    return distance


def targetted_dijkstra(graph, source_node, destination):
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
                # siftup the newly adjusted node until properly placed to preserve heap invariance
                ## essentially linear method
                hq.heapify(unvisited)
                ## heap method
                # hq._siftdown(unvisited, 0, neighbour_index)
            print(unvisited)
    return distance


# helper function that traces back through the previous nodes and compiles the steps needed to be taken
# to get from source to destination.
def _unpack_path_to_node(previous_node_dictionary, source_node, destination_node):
    # last node checked in the chain
    last_node = destination_node
    # initialize empty path array
    path = []
    while (last_node != source_node):
        # add last node to path
        path.insert(0, last_node)
        # update last node
        last_node = previous_node_dictionary[last_node]
        # check to see if there even is a connection
        if last_node == None:
            return None
    # insert source node to the path
    path.insert(0, source_node)
