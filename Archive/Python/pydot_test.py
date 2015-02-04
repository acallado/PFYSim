import pydot
graph = pydot.Dot('graphname', graph_type='digraph') 
pmo100 = pydot.Node("PMO-100")
sa300 = pydot.Node("SA-300")
sa100 = pydot.Node("SA-100")
sa200 = pydot.Node("SA-200")
graph.add_edge(pydot.Edge(pmo100, sa300))
graph.add_edge(pydot.Edge(sa100, sa300))
graph.add_edge(pydot.Edge(sa100, sa200))
graph.add_edge(pydot.Edge(pmo100, sa100))
graph.write_png('example1_graph.png')
