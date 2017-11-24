# Required packages

This code requires python package NetworkX
Please follow these instructions to install the package first:
(https://networkx.github.io/documentation/networkx-1.10/install.html)


The package also requires the installation of multiple other packages including:
* `numpy`
* `scipy`
* `matplotlib` etc...

Additionally, you will need these python packages:
* `getopt`
* `pickle`
* `texttable`

# Graph Generator

Run the following CLI commands in `src` to generate a graph/or graphs with the following format :

{
  node0: {node1:weight0_1, node2:weight0_2}
  node1: ...
}

(it is a dictionary of dictionaries)

```python
graph = {0 : {1:6, 2:8},
         1 : {4:11},
         2 : {3: 9},
         3 : {},
         4 : {5:3},
         5 : {2: 7, 3:4}}
```
The graphs are saved as pickle files in the `graphs/` folder which is automatically created upon runtime.

**Generate a graph with 10000 nodes and edge probability of 20%**
```bash
python3 graph generator -p 0.2 -n 10000
``` 
**Generate a graph with 2000 nodes and edge probability of 50%**
```bash
python3 graph generator --probability=0.5 --nodes=2000
``` 

**Generate a graph with 10 nodes, edge probability of 50%**
Also generates plot of the graph
```bash
python3 graph generator --probability=0.5 --nodes=2000 -d
``` 

**Generate all graphs with 10, 100, 500, 1000, 2000, 5000, 10000, 15000 nodes**
```bash
cd src
python3 graph generator --probability=0.2 -a 
``` 

> Be careful about running a large number of nodes with a high edge probability!!
> If your computer does not have the required memory, the script will kill itself
> Creating a graph with 15000 nodes and edge probability of 50% has failed on a decent computer (16GB RAM)
> Creating a graph with 20000 nodes and edge probability of 20% has failed on a decent computer (16GB RAM)


**Example output of graph generation**

```
python3 graph_generator -p 0.2 -n 15000

--------------------- 15000 nodes ---------------------
Generating weightless graph with 15000 nodes and an edge probability of 0.2...
Number of edges: 22496801
Generated graph!
Setting random weights between 5 and 50 to all edges...
Edge weights set!
Graph generated in 180.35305 seconds!
Formatting graph...
Loop: 14999, Runtime: 85.06316
Runtime: 265.42249
```

**Example of plot**

![alt text](https://raw.githubusercontent.com/GamerAlien/ECSE-414-G13/floydwarshall/example.png)

# Testing environment

All the following algorithms are given s source node 0 and a target node for them to search for shortest path.
The target node is always the last node from the generated graph (ie. 9, 99, 199, 4999 etc..)

## Dijkstra

In our code, Dijkstra is greedy meaning that it will stop after having found its shortest path
To execute a regular Dijkstra, simply comment the lines 117-118 in `src/dijkstra.py`

```python
if current_node == goal_node:
    return reconstruct_path(cameFrom, current_node), gScore[goal_node]
```
This algorithm's complexity depends on the heuristic

## A*

This algorithm is the same as Dijkstra with the addition of heuristic
The heuristic generation is not included in the runtime calculation
In our code, A* is greedy meaning that it will stop after having found its shortest path
To execute a regular A*, simply comment the lines 67-68 in `src/astar.py`

```python
if current_node == goal_node:
    return reconstruct_path(cameFrom, current_node), gScore[goal_node]
```
This algorithm has a complexity of O(V^3)

## Floyd-Warshall

This algorithm has a complexity of O(V^3)
For a graph with a maximum of 15 nodes, you can uncomment the lines 93-97 in `src/floydwarshall.py` to vizualize the distance matrix and the predecessor matrix

```python
#if (len(dist) <= 15):
#     print("Shortest distance matrix from each vertex:\n")
#     printMatrix(dist.copy());
#     print("\nPredecesors matrix in shortest path:\n")
#     printMatrix(pred.copy(), False);
```

**Example of matrix vizualization**

```bash
Distance matrix 

+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| / |   0   |   1   |   2   |   3   |   4   |  5   |  6   |  7   |  8   |  9   |
+===+=======+=======+=======+=======+=======+======+======+======+======+======+
| 0 | 0->0  | 0->1  | 0->2  | 0->3  | 0->4  | 0->5 | 0->6 | 0->7 | 0->8 | 0->9 |
|   | : 0   | : 5   | : 26  | : 46  | : 52  | : 52 | : 61 | : 40 | : 41 | : 19 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 1 | 1->0  | 1->1  | 1->2  | 1->3  | 1->4  | 1->5 | 1->6 | 1->7 | 1->8 | 1->9 |
|   | : 5   | : 0   | : 21  | : 41  | : 47  | : 47 | : 56 | : 45 | : 36 | : 14 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 2 | 2->0  | 2->1  | 2->2  | 2->3  | 2->4  | 2->5 | 2->6 | 2->7 | 2->8 | 2->9 |
|   | : 26  | : 21  | : 0   | : 20  | : 54  | : 26 | : 63 | : 66 | : 15 | : 35 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 3 | 3->0  | 3->1  | 3->2  | 3->3  | 3->4  | 3->5 | 3->6 | 3->7 | 3->8 | 3->9 |
|   | : 46  | : 41  | : 20  | : 0   | : 73  | : 45 | : 82 | : 86 | : 35 | : 55 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 4 | 4->0  | 4->1  | 4->2  | 4->3  | 4->4  | 4->5 | 4->6 | 4->7 | 4->8 | 4->9 |
|   | : 52  | : 47  | : 54  | : 73  | : 0   | : 28 | : 9  | : 92 | : 52 | : 61 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 5 | 5->0  | 5->1  | 5->2  | 5->3  | 5->4  | 5->5 | 5->6 | 5->7 | 5->8 | 5->9 |
|   | : 52  | : 47  | : 26  | : 45  | : 28  | : 0  | : 37 | : 92 | : 24 | : 61 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 6 | 6->0  | 6->1  | 6->2  | 6->3  | 6->4  | 6->5 | 6->6 | 6->7 | 6->8 | 6->9 |
|   | : 61  | : 56  | : 63  | : 82  | : 9   | : 37 | : 0  | :    | : 61 | : 70 |
|   |       |       |       |       |       |      |      | 101  |      |      |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 7 | 7->0  | 7->1  | 7->2  | 7->3  | 7->4  | 7->5 | 7->6 | 7->7 | 7->8 | 7->9 |
|   | : 40  | : 45  | : 66  | : 86  | : 92  | : 92 | :    | : 0  | : 81 | : 37 |
|   |       |       |       |       |       |      | 101  |      |      |      |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 8 | 8->0  | 8->1  | 8->2  | 8->3  | 8->4  | 8->5 | 8->6 | 8->7 | 8->8 | 8->9 |
|   | : 41  | : 36  | : 15  | : 35  | : 52  | : 24 | : 61 | : 81 | : 0  | : 50 |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+
| 9 | 9->0  | 9->1  | 9->2  | 9->3  | 9->4  | 9->5 | 9->6 | 9->7 | 9->8 | 9->9 |
|   | : 19  | : 14  | : 35  | : 55  | : 61  | : 61 | : 70 | : 37 | : 50 | : 0  |
+---+-------+-------+-------+-------+-------+------+------+------+------+------+

Predecesors matrix in shortest path:

+---+----+----+----+----+----+----+----+----+----+----+
| / | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |
+===+====+====+====+====+====+====+====+====+====+====+
| 0 | -1 | 0  | 1  | 2  | 1  | 2  | 4  | 0  | 2  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 1 | 1  | -1 | 1  | 2  | 1  | 2  | 4  | 0  | 2  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 2 | 1  | 2  | -1 | 2  | 5  | 2  | 4  | 0  | 2  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 3 | 1  | 2  | 3  | -1 | 5  | 3  | 4  | 0  | 2  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 4 | 1  | 4  | 5  | 5  | -1 | 4  | 4  | 0  | 5  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 5 | 1  | 2  | 5  | 5  | 5  | -1 | 4  | 0  | 5  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 6 | 1  | 4  | 5  | 5  | 6  | 4  | -1 | 0  | 5  | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 7 | 7  | 0  | 1  | 2  | 1  | 2  | 4  | -1 | 2  | 7  |
+---+----+----+----+----+----+----+----+----+----+----+
| 8 | 1  | 2  | 8  | 2  | 5  | 8  | 4  | 0  | -1 | 1  |
+---+----+----+----+----+----+----+----+----+----+----+
| 9 | 1  | 9  | 1  | 2  | 1  | 2  | 4  | 9  | 2  | -1 |
+---+----+----+----+----+----+----+----+----+----+----+
```

# Testing procedure

> To run the tests make sure that you have generated all appropriate graphs, else the tests might not run


The following tests will generate a txt result file in `results/` which is updated whenever a new test is run.
Different results files will be generated according to the algorithm run and the edge probability.

> The pickle files inside the results directory serve as a history for the previous results, DO NOT ERASE THEM if you wish to keep updating your results files



Run the following commands to test the algorithms in the `test` directory:

## FloydWarshall

Runs Floyd-Warshall on the 100 nodes graph with 20% edge probability
```
python3 test_fw.py -p 0.20 -n 100
```

**Output**
```
--------------------- 100 nodes ---------------------
Finding shortest path from 0 to 99...
Loop: 99, Runtime: 0.30331
-> Shortest Path: 	0->75->99

-> Cost:		22

-> Runtime: 		0.30608 seconds

+------------+-----------+------+-----------------+
| Graph size |   Path    | Cost |     Runtime     |
+============+===========+======+=================+
| 100 nodes  | 0->75->99 |  22  | 0.30608 seconds |
+------------+-----------+------+-----------------+
```
Results file: `results/resultsFW_20percent.txt`

## A*

* Runs A* on the 1000 and 2000 nodes graph with 50% edge probability
```
python3 test_as.py -p 0.50 -n 1000
python3 test_as.py -p 0.50 -n 2000
```

**Output**
```
creating new table
--------------------- 1000 nodes ---------------------
Finding shortest path from 0 to 999...
Iteration: 650, Runtime: 4.79784
-> Shortest Path: 	[0, 104, 999]
-> Cost:		15
-> Runtime: 		4.7981 seconds

+------------+---------------+------+----------------+
| Graph size |     Path      | Cost |    Runtime     |
+============+===============+======+================+
| 1000 nodes | [0, 104, 999] |  15  | 4.7981 seconds |
+------------+---------------+------+----------------+

appending to old table results
--------------------- 2000 nodes ---------------------
Finding shortest path from 0 to 1999...
Iteration: 328, Runtime: 11.41803
-> Shortest Path: 	[0, 1767, 1999]
-> Cost:		12
-> Runtime: 		11.41852 seconds

+------------+---------------+------+----------------+
| Graph size |     Path      | Cost |    Runtime     |
+============+===============+======+================+
| 1000 nodes | [0, 104, 999] |  15  | 4.7981 seconds |
+------------+---------------+------+----------------+
| 2000 nodes |   [0, 1767,   |  12  |    11.41852    |
|            |     1999]     |      |    seconds     |
+------------+---------------+------+----------------+
```

The iteration number is the numbe of while loop iterations before reaching the target node.

## Dijkstra

* Runs Dijkstra on all the graphs generated with 0.3 percent edge probability
```
python3 test_dijkstra -p 0.3 -a
```

**Output**
```
--------------------- 10 nodes ---------------------
Iteration: 4, Runtime: 0.00032
-> Shortest Path: 	[0, 9]

-> Cost:		21

-> Runtime: 		0.00069 seconds

--------------------- 100 nodes ---------------------
No graph generated with 100nodes and 0.3edge probability!
Continuing to next execution if any...
--------------------- 200 nodes ---------------------
No graph generated with 200nodes and 0.3edge probability!
Continuing to next execution if any...
--------------------- 500 nodes ---------------------
Iteration: 290, Runtime: 0.25159
-> Shortest Path: 	[0, 94, 499]

-> Cost:		14

-> Runtime: 		0.25194 seconds

--------------------- 1000 nodes ---------------------
Iteration: 717, Runtime: 2.19646
-> Shortest Path: 	[0, 182, 248, 999]

-> Cost:		18

-> Runtime: 		2.19677 seconds

--------------------- 2000 nodes ---------------------
Iteration: 1883, Runtime: 22.19466
-> Shortest Path: 	[0, 1774, 1999]

-> Cost:		13

-> Runtime: 		22.1949 seconds

--------------------- 5000 nodes ---------------------
Iteration: 4049, Runtime: 357.15096
-> Shortest Path: 	[0, 3045, 4999]

-> Cost:		13

-> Runtime: 		357.15171 seconds
+------------+-----------+------+-----------------+
|  10 nodes  |  [0, 9]   |  21  | 0.00069 seconds |
+------------+-----------+------+-----------------+
| 500 nodes  |  [0, 94,  |  14  | 0.25194 seconds |
|            |   499]    |      |                 |
+------------+-----------+------+-----------------+
| 1000 nodes | [0, 182,  |  18  | 2.19677 seconds |
|            | 248, 999] |      |                 |
+------------+-----------+------+-----------------+
| 2000 nodes | [0, 1774, |  13  | 22.1949 seconds |
|            |   1999]   |      |                 |
+------------+-----------+------+-----------------+
| 5000 nodes | [0, 3045, |  13  |    357.15171    |
|            |   4999]   |      |     seconds     |
+------------+-----------+------+-----------------+

```

# Some Test Results


The following tests were run on a Dell XPS:
* 8x Intel(R) Core(™) i7-6700HQ CPU @2.6GHz
* 16GB RAM
* Run on Ubuntu 16.04LTS

Nodes |Algorithm | Path | Cost | Runtime | Iterations
----- | ---------------- | ----------------- | ---- | ---------- | -----------
10 | A* | 0, 2, 5, 9 | 39 | 0.00045 | 6
10 | Floyd-Warshall | 0, 2, 5, 9 | 34 | 0.00093 | N/A
10 | Dijkstra | 0, 2, 5, 9 | 39 | 0.00049 | 7
100 | A* | 0, 1, 3, 99 | 20 | 0.00263 | 22
100 | Floyd-Warshall | 0, 1, 3, 99 | 20 | 0.32351 | N/A
100 | Dijkstra | 0, 1, 3, 99 | 20 | 0.0049 | 35
500 | A* | 0, 161, 499 | 15 | 0.33082 | 170
500 | Floyd-Warshall | 0, 161, 499 | 15 | 36.94131 | N/A
500 | Dijkstra | 0, 161, 499 | 15 | 0.51513 | 267
1000 | A* | 0, 48, 999 | 15 | 4.77038 | 676
1000 | Floyd-Warshall | 0, 48, 999 | 15 | 288.87987 | N/A
1000 | Dijkstra | 0, 48, 999 | 15 | 5.70721 | 851
2000 | A* | 0, 214, 1999 | 12 | 0.89067 | 26
2000 | Floyd-Warshall |0, 214, 1999 | 12 | 2344.97588 | N/A
2000 | Dijkstra |0, 214, 1999 | 12 | 7.8211 | 228
