import pickle
import math
import time 

def get_heuristic(graph, node, goal_node):
	# TODO
	heuristic = 0 
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

def a_star(graph, start_node, goal_node):
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
	fScore[start_node] = get_heuristic(graph, start_node, goal_node)
	
	# List of discovered but unevaluated nodes and their estimated total costs
	# Initially, only start node is known
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
			fScore[neighbour] = gScore[neighbour] + get_heuristic(graph, neighbour, goal_node)
			
			# Discover new node
			if neighbour not in openSet:
				openSet[neighbour] = fScore[neighbour]


