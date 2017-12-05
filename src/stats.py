import matplotlib.pyplot as plt
import networkx as nx
import graph_generator as gg

from collections import Counter
from functools import reduce

def graphChars(G):

    def density(li):

        counter = Counter(li)
        x = []
        y = []

        for key in sorted(list(counter)):
            x.append(key)
            y.append(counter[key])

        return (x,y);

    w_list = list(map((lambda x: x[2]['weight']) ,G.edges(data=True)))
    g_size = len(list(G))
    print(g_size)
    d_list = list(map((lambda x: x[1]), G.degree()))#int(100 * x[1]/g_size)), G.degree()))

    w = density(w_list)
    d = density(d_list)

    plt.subplot(121)
    plt.bar(w[0],w[1])
    plt.xlabel('Weight')
    plt.ylabel('Number of edges')
    plt.subplot(122)
    plt.bar(d[0],d[1])
    plt.xlabel('Degree')
    plt.show()

def plotResults(alg_name, graph_sizes, results):

    plt.plot(graph_sizes, results)
    plt.xlabel('Graph size')
    plt.ylabel('Running time (ms)')
    plt.title(alg_name)
    plt.show()