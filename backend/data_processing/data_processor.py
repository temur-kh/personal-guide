from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def _create_connection(self):
        pass

    @abstractmethod
    def select_query(self, params):
        pass

    @abstractmethod
    def close_connection(self):
        pass