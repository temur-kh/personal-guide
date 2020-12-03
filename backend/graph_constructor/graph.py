from abc import ABC, abstractmethod


class Graph(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_way(self, route):
        pass

    @abstractmethod
    def save(self, file_name):
        pass

    @staticmethod
    def load(file_name):
        pass
