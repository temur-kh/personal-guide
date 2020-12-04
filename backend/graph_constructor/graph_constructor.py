from abc import ABC, abstractmethod


class GraphConstructor(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_graph(self, params, max_points=None):
        pass
