from abc import ABC, abstractmethod


class Optimizer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def solve(self):
        pass
