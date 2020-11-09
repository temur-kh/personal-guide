from optimizer.optimizer import Optimizer


class ORToolsOptimizer(Optimizer):

    graph = None

    def __init__(self, graph):
        super().__init__()
        self.graph = graph

    def solve(self):
        pass
