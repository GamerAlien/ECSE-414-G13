import pickle
import math
import time

def get_heuristic(graph, node, goal_node):
	h_dict = {
	'A': 2,
	'B': 2,
	'C': 2,
	'D': 1,
	'E': 1,
	'F': 0}
	heuristic = h_dict[node]
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

graph = {
'A':[('B',2),('E',10)], 
'B':[('A',2),('C',5),('E',7)], 
'C':[('B',5),('D',2)], 
'D':[('C',2),('F',1)], 
'E':[('A',10),('B',7),('D',2),('F',3)], 
'F':[('D',1),('E',3)]}

delay = 0.1

start_time = time.time()
path, cost = a_star(graph, 'A', 'F')
time.sleep(delay)
runtime = time.time() - start_time - delay

print('Optimal path:  ' + str(path))
print('Cost:          ' + str(cost))
print('Runtime:       ' + str(runtime))