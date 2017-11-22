#import dikstra

#TODO
def bfs(net, nodeA, nodeB):

#TODO
def greedy(net):

#Work in progress
def perfect(net):

    network = net['network']
    topography = net['topography']
    nodeToASMap = net['nodeToASMap']
    asList = net['asList']

    hGraph = {}
    for _as in range(0, len(topography)):
        hGraph[_as] = {}
        for neighbor in topography[_as]:
            hGraph[_as][neighbor] = {}
            for node in list(asList[_as].keys())
                hGraph[_as][neighbor][node] = dikstra.do(network, node, neighbor)


    def heuristic(nodeA, nodeB):
        asPath = bfs(topography,
            nodeToASMap[nodeA],
            nodeToASMap[nodeB])
            
        return hGraph[asPath[1]][nodeA] +
            reduce((lambda x, y: hGraph[x][y])), asPath[1:-1])
            hGraph[subnetPath[-1]][nodeB]

    return heuristic

    

