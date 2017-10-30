import networkx as nx
import matplotlib.pyplot as plt
import community as com
import numpy as np
from networkx.drawing.nx_pydot import write_dot

def revert_dict(d):
	new_d = {}
	for key, val in d.items():
		if val not in new_d:
			new_d[val] = []
		new_d[val].append(key)
	return new_d

def cnode(group):
	return 'cluster ' + str(group)

def new_graph(partition, graph):
	# Create new graph
	G = nx.MultiGraph()
	for group in partition.values():
		G.add_node(cnode(group))
	for i,j in graph.edges():
		G.add_edge(cnode(partition[i]), cnode(partition[j]))
	# Create a map to get back to the old graph 
	map_ = {}
	for key, val in partition.items():
		if cnode(val) not in map_:
			map_[cnode(val)] = []
		map_[cnode(val)].append(key)
	write_dot(G, 'multi.dot')
	return G, map_

def unfold(map__):
	hl = len(map__)-1 # Take note of the highest level
	lvl = lambda x: 'level ' + str(x)
	map_ = {}
	for cluster in map__[lvl(hl)]:
		map_[cluster] = map__[lvl(hl)][cluster]
	while hl > 0:
		hl -= 1
		for key in map_:
			new_val = []
			for elem in map_[key]:
				new_val += map__[lvl(hl)][elem]
			map_[key] = new_val
	return map_
		
def modularity(partition, graph, A, res=0.75):
	m2 = np.sum(A)
	s = 0 
	for i, ni in enumerate(graph):
		for j, nj in enumerate(graph):
			if partition[ni] == partition[nj]: 
				s += (A[i,j] if i != j else 2*A[i,j]) - res*graph.degree(ni)*graph.degree(nj)/m2
	return s/m2


def trivial_partition(graph):
	part = {}
	for i, node in enumerate(graph):
		part[node] = i
	return part

def agg(graph):
	part, adj = trivial_partition(graph), nx.to_numpy_matrix(graph)
	max_ = modularity(part, graph, adj)
	for node in graph:
		part_ = part
		val = part[node]
		for n in graph.neighbors(node):
			part_[node] = part[n]
			mod = modularity(part_, graph, adj)
			if mod > max_:
				val, max_ = part[n], mod
		part[node] = val
	for i, val in enumerate(set(part.values())):
		for key in part:
			if part[key] == val:
				part[key] = i	
	return part, max_

def detect(graph):
	G, part, map__, i, mod_ = graph, {}, {}, 0, -2
	while True:
		partition, mod = agg(G)
		print(revert_dict(partition), mod)
		G, map_ = new_graph(partition, G)
		map__['level '+ str(i)] = map_
		if mod <= mod_:
			break
		mod_ = mod
		i += 1
	print(map__['level '+str(len(map__)-1)])
	return partition, unfold(map__)

