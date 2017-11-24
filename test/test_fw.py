import pickle
import texttable
import sys
import getopt
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import floydwarshall


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


def executeFW(size, table, percent):
    print("--------------------- " + str(size) + " nodes ---------------------")
    # runtime = generateGraph(size)
    # print("Graph generation time: "+runtime+" 	seconds")
    graph = pickle.load(open(getFileName(size, percent), "rb"))
    # graph = final_network.getFormattedGraph(graph)
    print("Finding shortest path from 0 to " + str(size - 1) + "...")
    # print(graph)

    results = floydwarshall.getFloydWarshallResults(graph, 0, size - 1)
    print("\n-> Shortest Path: 	" + results['path'] + "\n")
    print("-> Cost:		" + results['cost'] + "\n")
    print("-> Runtime: 		" + results['runtime'] + " seconds\n")
    table.add_rows([[str(size) + ' nodes', results['path'], results['cost'], results['runtime'] + " seconds"]], False)
    return results


def floydwarshallTests(run_all, nodes, percent):
    try:
        tableFW = pickle.load(open("../results/results_table_FW_" + str(int(percent * 100)) + "percent.pickle", 'rb'))
    except:
        tableFW = texttable.Texttable()
        tableFW.set_cols_align(["c", "c", "c", "c"])
        tableFW.header(["Graph size", "Path", "Cost", "Runtime"])

    if run_all:
        executeFW(10, tableFW, percent)
        executeFW(100, tableFW, percent)
        executeFW(200, tableFW, percent)
        executeFW(500, tableFW, percent)
        executeFW(1000, tableFW, percent)
        executeFW(2000, tableFW, percent)
        executeFW(5000, tableFW, percent)
        executeFW(10000, tableFW, percent)
    else:
        executeFW(int(nodes), tableFW, percent)


    print(tableFW.draw())
    output(open("../results/resultsFW_" + str(int(percent * 100)) + "percent.txt", 'w+'), tableFW.draw())
    table_pickle = open("../results/results_table_FW_" + str(int(percent * 100)) + "percent.pickle", 'wb')
    pickle.dump(tableFW, table_pickle)


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

    floydwarshallTests(run_all,int(nodes), percent)

if __name__ == '__main__':
    main(sys.argv[1:])
