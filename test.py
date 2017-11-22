import floydwarshall
import network
import pickle
import time
import numpy as np
import texttable

def output(file_handle, message):
	# print(message)
	file_handle.write(str(message))

def getFileName(size):
	filename = "graphs/graph_"+str(size)+"_nodes.pickle"
	return filename

def generateGraph(size):
	start_time = time.time()
	netData = network.create(size)
	runtime = time.time() - start_time
	outfile = open(getFileName(size),'wb')
	pickle.dump(netData['network'],outfile)
	outfile.close()
	return str(np.around(runtime, decimals=5))

def execute(size, table):

	print("--------------------- "+str(size)+" nodes ---------------------")
	runtime = generateGraph(size)
	print("Graph generation time: "+runtime+" 	seconds")
	graph = pickle.load(open(getFileName(size), "rb" ))
	print("Finding shortest path from 0 to "+str(size-1)+"...")	
	results = floydwarshall.getFloydWarshallResults(graph, 0, size-1)
	print("-> Shortest Path: 	"+results['path'])
	print("-> Cost:		"+results['cost'])
	print("-> Runtime: 		"+results['runtime']+" seconds\n")
	table.add_rows([[str(size)+' nodes', results['path'], results['cost'], results['runtime']+" seconds"]], False)
	return results

def main():
	# t = 
	table = pickle.load(open("results/results_table.pickle", 'rb')) 
	print(table.draw())
	# table = texttable.Texttable()
	# table.set_cols_align(["c", "c", "c", "c"])
	# table.header(["Graph size", "Path", "Cost", "Runtime"])
	results = {}
	# results[10] = execute(10, table)
	# results[100] = execute(100, table)
	# results[500] = execute(500, table)
	# results[1000] = execute(1000, table)
	# results[2000] = execute(2000, table)
	results[5000] = execute(5000, table)
	# results[10000] = execute(10000, table)


	print(table.draw())
	output(open("results/results.txt", 'w+'), table.draw())
	table_pickle = open("results/results_table.pickle",'wb')
	pickle.dump(table, table_pickle)



 

if __name__ == '__main__':
    main()