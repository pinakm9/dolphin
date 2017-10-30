import igraph as ig
import louvain
G = ig.Graph.Read_GML("./../data/dolphins.gml")

# Louvain method
part = louvain.find_partition(G, method = "RBConfiguration", resolution_parameter = 0.5)
print part
color_dict = {0: "blue", 1: "green"}
shape_dict = {0: "circle", 1: "square"}
for i, nodes in enumerate(part):
	for node in nodes:
		G.vs[node]["comm"] = i
		G.vs[node]["color"] = color_dict[i]
		G.vs[node]["shape"] = shape_dict[i]
visual_style = {}
visual_style["vertex_size"] = 8
visual_style["vertex_color"] = G.vs["color"]
visual_style["vertex_label"] = G.vs["label"]
visual_style["layout"] = G.layout("kk")
visual_style["bbox"] = (800, 800)
visual_style["margin"] = 40
visual_style["vertex_label_dist"] = 1.2
visual_style["vertex_shape"] = G.vs["shape"]
ig.plot(G, 'louvain.pdf', **visual_style)

# Fiedler method