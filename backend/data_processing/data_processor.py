from abc import ABC, abstractmethod


class DataProcessor(ABC):

    source_name = ""

    def __init__(self, source_name):
        self.source_name = source_name

    @abstractmethod
    def create_connection(self):
        pass

    @abstractmethod
    def query(self, params):
        pass

    @abstractmethod
    def close_connection(self):
        pass
