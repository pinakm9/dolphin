import networkx as nx
import matplotlib.pyplot as plt
import community as com
from louvain import *
G = nx.read_gml('./../data/dolphins.gml')
part = com.best_partition(G, resolution=10)
G_,_ = new_graph(part, G)
p, m = detect(G)

print m
m_= revert_dict(part)
for k in m_:
	print len(m_[k]) 
#print agg(G)