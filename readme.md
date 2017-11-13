Installation
-----------

This code requires python package NetworkX
Please follow these instructions to install the package first:
(https://networkx.github.io/documentation/networkx-1.10/install.html)


The package also requires the installation of multiple other packages including `numpy`, `scipy`, `matplotlib` etc...

Usage
-----

To change the number of nodes, the probability of edge creation and weight range, edit the following line:
```
G = graph_generator.generateERGraph(nodes, edge_probability, start_range, end_range)
```

Then run the following command:


```
python3 floydwarshall.py
```

Output
------

```
Generating weightless graph with 200 nodes and an edge probability of 0.15...
Generated graph!
Setting random weights between 1 and 12 to all edges...
Edge weights set!
Graph generated in 0.02239 seconds!
Number of edges: 2981
Formatting graph...
Graph Formatted!
Creating adjacency matrix...
Created Adjacency matrix!
Started algorithm...
Done!
Cost:          5
Optimal path:  1->135->171->187->14->2
Runtime:       2.18968 seconds
```

The following plot is also generated:

![alt text](https://raw.githubusercontent.com/GamerAlien/ECSE-414-G13/floydwarshall/example_graph.png)
