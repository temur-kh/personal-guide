from abc import ABC, abstractmethod


class MLModel(ABC):

    x_train = None
    y_train = None

    def __init__(self):
        pass

    @abstractmethod
    def fit(self, x_train, y_train=None):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def fit_predict(self, x_train):
        pass
