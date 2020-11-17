from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_distance(self):
        pass

    @abstractmethod
    def get_way(self, path):
        pass
