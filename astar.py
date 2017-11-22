
import pickle
import math
import time

def generate_heuristic(graph, goal_node):
	# For each node, the minimum weight among all edges it is connected to
    min_costs = []

    # Determine smallest edge weight in graph
    print(graph)
    for node in graph:
        print(node)
        print("graph[node]: "+str(graph[node]))
        # print(key=lambda x: x[1])
        # min_costs.append(min(graph[node], key=lambda x: x[1])[1])
        min_costs.append(min(graph[node], key=lambda x: x[1])[1])
    lowest_cost = min(min_costs)
    
    # For each node, the minimum number of steps from the goal times the minimum edge weight
    heuristic = {}

    # Set of discovered nodes whose neighbours' heuristics must be calculated
    # Initially only goal node is known
    openSet = [goal_node]

    # Cost of going from goal to goal is 0
    heuristic[goal_node] = 0
    
    while openSet:
        node = openSet[0]
        neighbours = get_neighbours(graph, node)
        for neighbour in neighbours:

        	# Ignore neighbours whose heuristics have already been calculated
            if neighbour in heuristic:
                continue

            # Calculate heuristic for new node 
            heuristic[neighbour] = heuristic[node] + lowest_cost
            openSet.append(neighbour)
            
        # Node's neighbours have been evaluated
        del openSet[0]    
    return heuristic

def get_neighbours(graph, node):
	neighbours = []
	for i in range(0,len(graph[node])):
		neighbours.append(graph[node][i][0])
	return neighbours

def reconstruct_path(cameFrom, current_node):
	total_path = [current_node]
	while current_node in cameFrom:
		current_node = cameFrom[current_node]
		total_path.append(current_node)
	total_path.reverse()
	return total_path

def a_star(graph, start_node, goal_node, heuristic):
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
	fScore[start_node] = heuristic[start_node]
	
	# List of discovered but unevaluated nodes and their estimated total costs
	# Initially only start node is known
	openSet = {start_node: fScore[start_node]}

	# List of evaluated nodes
	closedSet = []
	
	while openSet:
		# Move to node with lowest estimated total cost
		current_node = min(openSet, key=openSet.get)
	
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
			prelim_gScore = gScore[current_node] + [item for item in graph[current_node] if item[0] == neighbour][0][1]
			

			if prelim_gScore >= gScore[neighbour]:
				# Not a better path
				continue

			# New best path
			cameFrom[neighbour] = current_node
			gScore[neighbour] = prelim_gScore
			fScore[neighbour] = gScore[neighbour] + heuristic[neighbour]
			
			# Discover new node
			if neighbour not in openSet:
				openSet[neighbour] = fScore[neighbour]