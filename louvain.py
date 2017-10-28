import networkx as nx
import matplotlib.pyplot as plt
import community as com
import numpy as np


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
	return G, map_

def unfold(map__):
	hl = len(map__)-1 # Take note of the highest level
	lvl = lambda x: 'level ' + str(x)
	map_ = {}
	for cluster in map__[lvl(hl)]:
		map_[cluster] = map__[lvl(hl)][cluster]
	while hl > 0:
		for key in map_:
			new_val = []
			for elem in map_[key]:
				new_val += map__[lvl(hl-1)][elem]
			map_[key] = new_val
		hl -= 1
	return map_
		
def modularity(partition, graph, A):
	m2 = np.sum(A)
	s = 0 
	for i, ni in enumerate(graph):
		for j, nj in enumerate(graph):
			if partition[ni] == partition[nj]: 
				s += A[i,j] - graph.degree(ni)*graph.degree(nj)/m2
	if s/m2 < -1:
		print partition 
	return s/m2

def place_node(node, graph):
	mod = {}
	for n in graph.neighbors(node):
		if n != node: # Deal with self-loops
			partition = {}
			for i, n_ in enumerate(graph):
				if n_ != node:
					partition[n_] = i
			partition[node] = partition[n]
			mod[n] = modularity(partition, graph)
	max_, n_ = -1, node
	for n in mod:
		if max_ < mod[n]:
			n_ = n
			max_ = mod[n]
	return [n_, max_]


def trivial_partition(graph):
	part = {}
	for i, node in enumerate(graph):
		part[node] = i
	return part

def agglomerate(graph):
	mod0 = modularity(trivial_partition(graph), graph)
	part, i = {}, 0
	for node in graph:
		frnd, mod = place_node(node, graph)
		print(mod, mod0)
		if mod > mod0:
			if frnd not in part:
				part[frnd] = i
				i += 1
			part[node] = part[frnd]
		else:
			part[node] = i
			i += 1
	return part 

def agg(graph):
	part, adj = trivial_partition(graph), nx.to_numpy_matrix(graph)
	for node in graph:
		part_, max_ = part, -2
		for n in graph:
			part_[node] = part[n]
			mod = modularity(part_, graph, adj)
			#print mod
			if mod > max_:
				frnd, max_ = n, mod
		part[node] = part[frnd]
	for i, val in enumerate(set(part.values())):
		for key in part:
			if part[key] == val:
				part[key] = i	
	return part

def detect(graph, level = 2):
	G, part, map__, i = graph, {}, {}, 0
	while True:
		partition = agg(G)
		l = partition.values()
		print(len(l))
		if len(partition.values()) <= level or i == 6:
			break
		G, map_ = new_graph(partition, G)
		map__['level '+ str(i)] = map_
		i += 1
	return partition, unfold(map__)

