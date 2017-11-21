import random
from functools import reduce

#Creates a topology describing the connections between autonomous systems
#This topology has a tree like structure
def createTopology(size):

    #Generate a tree
    def createTree(a, b):

        tree = [a]

        nextNodeToPlace = a+1
        while nextNodeToPlace < b:
            lastSubtreeNode = random.randint(nextNodeToPlace, b-1)
            tree.append(
                createTree(nextNodeToPlace, lastSubtreeNode+1))
            nextNodeToPlace = lastSubtreeNode + 1

        return tree

    tree = createTree(0,size)
    
    #Flatten the tree into a dictionary 
    def flattenTree(graph, tree):
        graph[tree[0]] = []
        for branch in tree[1:]:
            graph[tree[0]].append(branch[0])
            flattenTree(graph, branch)

    topology = {}

    flattenTree(topology, tree)

    #Make edges bidirectional
    for asA in list(topology.keys()):
        for asB in list(topology.keys())[asA:]:
            if asB in topology[asA]:
                topology[asB].append(asA)

    #Return topology
    return topology

#Adds an undirected edge (as two directed edges) with a random weight between nodeA and nodeB.
def add_edge(net, nodeA, nodeB):
    weight = random.randint(1,10)
    net[nodeA].append([nodeB, weight])
    net[nodeB].append([nodeA, weight])

#Implementation of the combination math operation
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce((lambda x, y: x * y), range(n, n-r, -1), 1)
    denom = reduce((lambda x, y: x * y), range(1, r+1), 1)
    return numer//denom

#Returns the probability of having (at least) an edge between nodeA and nodeB
def edge_prob(nodeADegree, nodeBDegree, totalDegree):
    n2 = totalDegree - nodeADegree
    n1 = n2 - nodeBDegree
    r = nodeADegree
    return 1 - ncr(n1, r) / ncr(n2, r)

#Greate an autonomous system (a.k.a a sub network)
def createAS(nodeIDStart, size):

    _as = {}
    degrees = []
    totalDegree = 0

    #Add nodes and generate an expected cardinality for each node
    for node in range(nodeIDStart, nodeIDStart + size):
        _as[node] = []
        nodeDegree = random.randint(size//4, 3*size//4)
        degrees.append((node, nodeDegree));
        totalDegree += nodeDegree

    #Add edges randomly based on the expected cardinality of each node
    for nodeX in degrees:
        for nodeY in degrees[degrees.index(nodeX)+1:]:
            if random.random() <= edge_prob(nodeX[1], nodeY[1], totalDegree):
                add_edge(_as, nodeX[0], nodeY[0])

    return _as

#Connects a group of autonomous systems as described by the topology
#Returns a bundle of information regarding the create network, including the network itself
def connectAS(topology, asList):

    net = {}
    nodeToASMap = {}
    interASEdgeList = []

    for _as in range(0, len(asList)):
        for node in list(asList[_as].keys()):
            net[node] = asList[_as][node]
            nodeToASMap[node] = _as

    asIndexList = list(topology.keys())
    for _as in asIndexList:
        for neighbor in topology[_as]:
            if neighbor > _as:
                nodeA = random.choice(list(asList[_as].keys()))
                nodeB = random.choice(list(asList[neighbor].keys()))
                interASEdgeList.append({
                    'asA': _as,
                    'asB': neighbor,
                    'nodeA': nodeA,
                    'nodeB': nodeB
                })
                add_edge(net, nodeA, nodeB)

    return {'network' : net, 'nodeToASMap' : nodeToASMap, 'interASEdgeList' : interASEdgeList}

#Creates an entire network of the specified size
def create(size):

    MIN_NUM_AS = 4
    MAX_NUM_AS = 10

    nextNodeToCreate = 0
    asList = []

    while nextNodeToCreate < size:

        newASSize = random.randint(
            min(size - nextNodeToCreate,
                size // MAX_NUM_AS),
            min(size - nextNodeToCreate,
                size // MIN_NUM_AS))

        asList.append(createAS(nextNodeToCreate, newASSize))
        nextNodeToCreate += newASSize

    topology = createTopology(len(asList))

    
    netData = connectAS(topology, asList)
    netData['topology'] = topology
    netData['asList'] = asList
    
    return netData

