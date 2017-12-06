import pickle
import time
import numpy as np
import texttable
import sys
import getopt
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import astar



def output(file_handle, message):
    file_handle.write(str(message))


def getFileName(size, percent):
    if percent == 0.2:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx_20percent.pickle"
    elif percent == 0.5:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx.pickle"
    else:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx_" + str(int(percent * 100)) + "percent.pickle"
    return filename


def executeAS(size, table, percent):
    print("--------------------- " + str(size) + " nodes ---------------------")

    try:
        graph = pickle.load(open(getFileName(size, percent), "rb"))
    except:
        print('No graph generated with '+str(size)+'nodes and '+str(percent)+'edge probability!')
        print('Continuing to next execution if any...')
        return None
    # graph = final_network.getFormattedGraph(graph)
    print("Finding shortest path from 0 to " + str(size - 1) + "...")
    # print(graph)

    delay = 0.1

    h = astar.generate_heuristic(graph, size - 1)
    start_time = time.time()
    path, cost = astar.a_star(graph, 0, size - 1, h)

    # h = astar.generate_heuristic(graph, 'F')
    # path, cost = astar.a_star(graph, 'A','F', h)
    time.sleep(delay)
    runtime = time.time() - start_time - delay

    results = {'path': str(path), 'cost': str(cost), 'runtime': str(np.around(runtime, decimals=5))}

    print("\n-> Shortest Path: 	" + results['path'])
    print("-> Cost:		" + results['cost'])
    print("-> Runtime: 		" + results['runtime'] + " seconds\n")
    table.add_rows([[str(size) + ' nodes', results['path'], results['cost'], results['runtime'] + " seconds"]], False)
    return results

def execute_iteration(size, percent):
    try:
        graph = pickle.load(open(getFileName(size, percent), "rb"))
    except:
        print('failed to open graph pickle, aborting...')
        return None

    results_file_name = "../results/astar_results.csv"
    results_file = open(results_file_name, 'a')
    delay = 0.1
    for i in range(1, 10):
        node_number = i * size / 10
        start_time_heuristic = time.time()
        h = astar.generate_heuristic(graph, node_number)
        time.sleep(delay)
        heuristic_runtime = time.time() - start_time_heuristic - delay
        start_time = time.time()
        path, cost, iteration = astar.a_star(graph, 0, node_number, h)
        time.sleep(delay)
        runtime = time.time() - start_time - delay
        results = str(size) + ',' + str(percent) + ',' + str(node_number) + ',' + str(runtime) +','+str(heuristic_runtime)+ ',' + str(
            iteration) + ',' + str(path) + '\n'
        results_file.write(results)

def test_all(sizes):
    # sizes = [10, 100, 500, 1000, 2000, 5000, 10000, 15000]
    percents = [0.2, 0.5]
    # clear results file
    results_file_name = "../results/astar_results.csv"
    results_file = open(results_file_name, 'w').close()
    for size in sizes:
        for percent in percents:
            execute_iteration(size, percent)

def astarTests(run_all, nodes, percent):
    try:
        h = open("../results/results_table_AS_" + str(int(percent * 100)) + "percent.pickle", 'rb')
        tableAS = pickle.load(h)
        print("appending to old table results")
    except:
        print("creating new table")
        tableAS = texttable.Texttable()
        tableAS.set_cols_align(["c", "c", "c", "c"])
        tableAS.header(["Graph size", "Path", "Cost", "Runtime"])
    # print(tableAS.draw())

    # resultsAS = {}
    # executeAS(nodes, tableAS, percent)
    if run_all:
        executeAS(10, tableAS, percent)
        executeAS(100, tableAS, percent)
        executeAS(200, tableAS, percent)
        executeAS(500, tableAS, percent)
        executeAS(1000, tableAS, percent)
        executeAS(2000, tableAS, percent)
        executeAS(5000, tableAS, percent)
        executeAS(10000, tableAS, percent)
        # astarTests(10000, percent)
    else:
        executeAS(int(nodes), tableAS, percent)

    output(open("../results/resultsAS_" + str(int(percent * 100)) + "percent.txt", 'w+'), tableAS.draw())
    try:
        h.close()
    except:
        pass
    table_pickle = open("../results/results_table_AS_" + str(int(percent * 100)) + "percent.pickle", 'wb')
    pickle.dump(tableAS, table_pickle)
    print(tableAS.draw())


def main(argv):

    if not os.path.exists("../results/"):
        print("Created results directory!")
        os.mkdir("../results/")
    optlist, argv = getopt.getopt(argv, 'p:n:a', ['probability=', 'nodes='])

    percent = 0.20
    run_all = False
    nodes = 10
    for opt, arg in optlist:
        if opt in ('-p', '--probability'):
            try:
                if float(arg) < 0 or float(arg) > 1:
                    print("ERROR: probability not valid: use 0.2, 0.5...")
                    sys.exit(2)
                percent = float(arg)
            except:
                print("ERROR: Invalid probability!")
                sys.exit(2)
        elif opt in ('-n', '--nodes'):
            nodes = arg
        elif opt == '-a':
            run_all = True

    astarTests(run_all, int(nodes), percent)

if __name__ == '__main__':
    main(sys.argv[1:])
