import pickle
import random
import sys

PARA_FILENAME = 'parameters.txt'
OUT_FILENAME = 'graph.pickle'

NODE_NUM = 'NumberOfNodes'
SUBNET_D_M = 'MeanSubnetDepth'
SUBNET_D_SD = 'SubnetDepthStandardDeviation'
SUBNET_NUM_M = 'MeanNumberOfSubnets'
SUBNET_NUM_SD = 'NumberOfSubnetsStandardDeviation'
NODE_D_M = 'MeanNodeDegree'
NODE_D_SD = 'NodeDegreeStandardDeviation'
EDGE_W_M = 'MeanEdgeWeight'
EDGE_W_SD = 'EdgeWeightStandardDeviation'

#Extracts the parameters form the parameters file.
#Reurns a dictionary of parameters
def load_para(filename):
    parameters = {}  #The parameter dictionary

    para_file = open(filename,'r')  #Open the parameter file

    while True:
        para_str = p_file.readline()  #Read the next line in the file

        #Break from the loop when no more lines can be read
        if len(para_str) == 0:
            break

        parameter = para_str.split(':')                 #Obtain the parameter tuple {paramater_name : parameter_value}
        parameters += parameter[0], parameter[1]        #Add the parameter to the dictionary
    
    para_file.close()   #Close the parameter file
    return parameters   #Return the dictionary

#Organises the list of nodes into a topology of subnetworks
def mk_subnet_topo(nodes, parameters, snet_depth):
    netheight = random.normalvariate(snet_depth, parameters['subnet depth mean'])  #The 'expected' number of nested subnetworks within this network

    topo = {}           #The topology of subnetworks
    topo.subnets = []   #The list of subnetworks directly under this one

    #If their is at least one subnetwork
    if netheight >= 1:
        member_num =  len(nodes) * min(random.normalvariate(            #Get the number of nodes that are members of this network
            snet_depth,
            parameters[SUBNET_D_SD]), 100)/100

        subnet_num = random.normalvariate(parameters[SUBNET_NUM_M],     #Get the number of subnetworks under this network
            parameters[SUBNET_NUM_SD])

        subnet_node_num = (len(nodes)-member_num)/subnet_num            #Calculate the number of nodes per subnetwork
        topo.members = nodes[:member_num]                               #Populate the list of member nodes
        snet_depth -= 1                                                 #Decrement the mean subnetwork depth's by one for recursive calls

        #All subnetworks but one get subnet_node_num nodes
        if netheight >= 2:
            for x in range(0,subnet_num-2):
                topo.subnets += subdivnet(
                    nodes[member_num + (x)*subnet_node_num:][:subnet_node_num],
                    x,
                    net_s, snet_n, snet_d)
        
        #The last subnetwork gets the remaining nodes
        topo.subnets += subdivnet(
            nodes[member_num + (subnet_num-1)*subnet_node_num:],
            subnet_num-1,
            net_s, snet_n, snet_d)

    #Else, all the nodes in the list are members of this network
    else:
        topo.members = nodes
    
    return topo  #Return the topography

#Adds an undirected edge (as two directed edges) with a random weight between nodeA and nodeB.
def add_edge(graph, parameters, nodeA, nodeB):
    weight = random.normalvariate(parameters[EDGE_W_M], parameters[EDGE_W_SD])
    graph[nodeA] += nodeB, weight
    graph[nodeB] += nodeA, weight

#Implementation of the combination math operation
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce((lambda x, y: x * y)), range(n, n-r, -1))
    denom = reduce((lambda x, y: x * y), range(1, r+1))
    return numer//denom

#Returns the probability of having (at least) an edge between nodeA and nodeB
def edge_prob(nodeA_degree, nodeB_degree, total_degree):
    n2 = total_degree - nodeA_degree
    n1 = n2 - nodeB_degree
    r = nodeA_degree
    return 1 - ncr(n1, r) // ncr(n2, r)

#Randomly connects all of the nodes. Nodes are
def connect_nodes(graph, parameters, net):

    degrees = []
    total_degree = 0
    for node in net.members:
        degrees += node, random.normalvariate(
            parameters[NODE_D_M],
            parameters[NODE_D_SD])
        total_degree += degrees[-1]

    for nodeX in degrees:
        for nodeY in degrees[nodeX+1:]:
            if random.random() >= edge_prob(nodeX[1], nodeY[1], total_degree):
                add_edge(graph, parameters, nodeX[0], nodeY[0])

    #Connect network to its subnetworks
    for subnet in net.subnet:
        connect_nodes(graph, parameters, subnet)
        add_edge(graph, parameters,
            random.choice(net.members),
            random.choice(subnet.members))

#Generates a new graph
def generate_graph(parameters):
    random.seed(p.seed)
    nodes = []
    graph = {}
    for node in range(0,parameters[NODE_NUM]):
        nodes += node
        graph += node, []

    subnet_topo = mk_subnet_topo(nodes, parameters, parameters[SUBNET_D_M])

    return connect_nodes(graph, parameters, subnet_topo)

#Main method
def main():
    if len(sys.argv)>=1:
        parafile = loadpara(sys.argv[1])
    else:
        parafile = loadpara(PARA_FILE)

    if len(sys.argv)>=2:
        outfile = open(sys.argv[2],'wb')
    else:
        outfile = open(OUT_FILENAME,'wb')
    
    network = generate_graph(loadpara(parafile))
    pickle.dump(network,outfile)
    parafile.close()
    outfile.close()
