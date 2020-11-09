from ml_module.base_ml_model import MLModel


class ClusteringModel(MLModel):

    def __init__(self):
        super().__init__()

    def transform(self):
        pass

    def fit(self, x_train, y_train=None):
        self.x_train = x_train
        self.y_train = y_train
        pass

    def predict(self):
        pass

    def fit_predict(self, x_train):
        self.fit(x_train)
        return self.predict()

