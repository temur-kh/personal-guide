from Create_graph.centrality import centrality
from Create_graph.reward import reward
from Create_graph.stop_time import stop_time
from Create_graph.simplification_graph import simplify_graph, matrix
from Create_graph.translator import translate


def create_graph():
    simplify_graph()
    matrix()
    centrality()
    stop_time()
    translate()
    reward()