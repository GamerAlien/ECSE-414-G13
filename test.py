import floydwarshall
import network
import pickle
import time
import numpy as np
import texttable
import astar

def output(file_handle, message):
	file_handle.write(str(message))

def getFileName(size):
	filename = "graphs/graph_"+str(size)+"_nodes_networkx.pickle"
	return filename

def executeAS(size, table):
	print("--------------------- "+str(size)+" nodes ---------------------")

	graph = pickle.load(open(getFileName(size), "rb" ))
	print("Finding shortest path from 0 to "+str(size-1)+"...")	

	graph = {
'A':[('B',2),('E',10)], 
'B':[('A',2),('C',5),('E',7)], 
'C':[('B',5),('D',2)], 
'D':[('C',2),('F',1)], 
'E':[('A',10),('B',7),('D',2),('F',3)], 
'F':[('D',1),('E',3)]}

	delay = 0.1

	start_time = time.time()
	h = astar.generate_heuristic(graph, size-1)
	path, cost = astar.a_star(graph, 0,size-1, h)
	time.sleep(delay)
	runtime = time.time() - start_time - delay

	results = {'path': str(path), 'cost': str(cost), 'runtime':str(np.around(runtime, decimals=5))}

	print("-> Shortest Path: 	"+results['path'])
	print("-> Cost:		"+results['cost'])
	print("-> Runtime: 		"+results['runtime']+" seconds\n")
	table.add_rows([[str(size)+' nodes', results['path'], results['cost'], results['runtime']+" seconds"]], False)
	return results

def executeFW(size, table):

	print("--------------------- "+str(size)+" nodes ---------------------")
	# runtime = generateGraph(size)
	# print("Graph generation time: "+runtime+" 	seconds")
	graph = pickle.load(open(getFileName(size), "rb" ))
	print("Finding shortest path from 0 to "+str(size-1)+"...")	
	results = floydwarshall.getFloydWarshallResults(graph, 0, size-1)
	print("-> Shortest Path: 	"+results['path'])
	print("-> Cost:		"+results['cost'])
	print("-> Runtime: 		"+results['runtime']+" seconds\n")
	table.add_rows([[str(size)+' nodes', results['path'], results['cost'], results['runtime']+" seconds"]], False)
	return results

def floydwarshallTests():
	try:
		tableFW = pickle.load(open("results/results_table_FW.pickle", 'rb')) 
	except:
		tableFW = texttable.Texttable()
		tableFW.set_cols_align(["c", "c", "c", "c"])
		tableFW.header(["Graph size", "Path", "Cost", "Runtime"])
	
	print(tableFW.draw())
	
	resultsFW = {}
	resultsFW[10] = executeFW(10, tableFW)
	# resultsFW[100] = executeFW(100, tableFW)
	# resultsFW[500] = executeFW(500, tableFW)
	# resultsFW[1000] = executeFW(1000, tableFW)
	# resultsFW[2000] = executeFW(2000, tableFW)
	# resultsFW[5000] = executeWF(5000, tableFW)
	# resultsFW[10000] = executeFW(10000, tableFW)

	print(tableFW.draw())
	output(open("results/resultsFW.txt", 'w+'), tableFW.draw())
	table_pickle = open("results/results_table_FW.pickle",'wb')
	pickle.dump(tableFW, table_pickle)

def astarTests():
	try:
		tableAS = pickle.load(open("results/results_table_AS.pickle", 'rb')) 
	except:
		tableAS = texttable.Texttable()
		tableAS.set_cols_align(["c", "c", "c", "c"])
		tableAS.header(["Graph size", "Path", "Cost", "Runtime"])
	
	print(tableAS.draw())

	resultsAS = {}
	resultsAS[10] = executeAS(10, tableAS)
	# resultsAS[100] = executeAS(100, tableAS)
	# resultsAS[500] = executeAS(500, tableAS)
	# resultsAS[1000] = executeAS(1000, tableAS)
	# resultsAS[2000] = executeAS(2000, tableAS)
	# resultsAS[5000] = executeAS(5000, tableAS)
	# resultsAS[10000] = executeAS(10000, tableAS)

	print(tableAS.draw())
	output(open("results/resultsAS.txt", 'w+'), tableAS.draw())
	table_pickle = open("results/results_table_AS.pickle",'wb')
	pickle.dump(tableAS, table_pickle)

def main():
	# floydwarshallTests()
	astarTests()


if __name__ == '__main__':
    main()