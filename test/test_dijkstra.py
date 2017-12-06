import pickle
import time
import numpy as np
import texttable
import sys
import getopt
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import dijkstra


def output(file_handle, message):
    file_handle.write("\n" + str(message))


def getFileName(size, percent):
    if percent == 0.2:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx_20percent.pickle"
    elif percent == 0.5:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx.pickle"
    else:
        filename = "../graphs/graph_" + str(size) + "_nodes_networkx_" + str(int(percent * 100)) + "percent.pickle"
    return filename


def executeD(size, table, percent):
    print("--------------------- " + str(size) + " nodes ---------------------")
    # runtime = generateGraph(size)
    # print("Graph generation time: "+runtime+" 	seconds")
    try:
        graph = pickle.load(open(getFileName(size, percent), "rb"))
    except:
        print('No graph generated with ' + str(size) + 'nodes and ' + str(percent) + 'edge probability!')
        print('Continuing to next execution if any...')
        return None
    # graph = final_network.getFormattedGraph(graph)
    delay = 0.1

    start_time = time.time()
    path, cost = dijkstra.dijkstra(graph, 0, size - 1)

    time.sleep(delay)
    runtime = time.time() - start_time - delay

    results = {'path': str(path), 'cost': str(cost), 'runtime': str(np.around(runtime, decimals=5))}

    print("\n-> Shortest Path: 	" + results['path'] + "\n")
    print("-> Cost:		" + results['cost'] + "\n")
    print("-> Runtime: 		" + results['runtime'] + " seconds\n")
    table.add_rows([[str(size) + ' nodes', results['path'], results['cost'], results['runtime'] + " seconds"]], False)
    return results


def execute_iteration(size, percent):
    try:
        graph = pickle.load(open(getFileName(size, percent), "rb"))
    except:
        print('failed to open graph pickle, aborting...')
        return None

    results_file_name = "../results/dijkstra_results.csv"
    results_file = open(results_file_name, 'a')
    delay = 0.1
    for i in range(1, 10):
        node_number = i * size / 10
        start_time = time.time()
        path, cost, iteration = dijkstra.dijkstra(graph, 0, node_number)
        time.sleep(delay)
        runtime = time.time() - start_time - delay
        results = str(size) + ',' + str(percent) + ',' + str(node_number) + ',' + str(runtime) + ',' + str(
            iteration) + ',' + str(path) + '\n'
        results_file.write(results)


def test_all():
    # sizes = [10, 100, 500, 1000, 2000, 5000, 10000, 15000]
    sizes = [5000]
    percents = [0.2, 0.5]
    # clear results file
    results_file_name = "../results/dijkstra_results.csv"
    results_file = open(results_file_name, 'w').close()
    for size in sizes:
        for percent in percents:
            execute_iteration(size, percent)


def dijkstraTests(run_all, nodes, percent):
    try:
        h = open("../results/results_table_D_" + str(int(percent * 100)) + "percent.pickle", 'rb')
        tableD = pickle.load(h)
        print("appending to old table results")
        h.close()
    except:
        print("creating new table")
        tableD = texttable.Texttable()
        tableD.set_cols_align(["c", "c", "c", "c"])
        tableD.header(["Graph size", "Path", "Cost", "Runtime"])

    if run_all:
        executeD(10, tableD, percent)
        executeD(100, tableD, percent)
        executeD(200, tableD, percent)
        executeD(500, tableD, percent)
        executeD(1000, tableD, percent)
        executeD(2000, tableD, percent)
        executeD(5000, tableD, percent)
        # executeD(10000, tableD, percent)
    else:
        executeD(int(nodes), tableD, percent)

    print(tableD.draw())
    output(open("../results/resultsD_" + str(int(percent * 100)) + "percent.txt", 'w+'), tableD.draw())

    table_pickle = open("../results/results_table_D_" + str(int(percent * 100)) + "percent.pickle", 'wb')
    pickle.dump(tableD, table_pickle)


def main(argv):
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

    dijkstraTests(run_all, int(nodes), percent)


if __name__ == '__main__':
    main(sys.argv[1:])
