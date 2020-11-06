from abc import ABC, abstractmethod


class MLModel(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def predict(self):
        pass
