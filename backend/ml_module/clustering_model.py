from sklearn.cluster import KMeans

from ml_module.base_ml_model import MLModel
import math

class ClusteringModel(MLModel):
    """
    Класс для кластеризации точек на карте.

    Attributes:
        model(sklearn.cluster) - модель для кластеризации.
        params(dict) - параметря для модели.
        x_train(2-d array-like) - таблица с признаками объектов.
    """
    model = None
    params = None

    def __init__(self, model=KMeans, params=None):
        """
        Создание модели для кластеризации

        Params:
            model(sklearn.cluster) - модель для кластеризации.
            params(dict) - параметря для модели.
        """

        super().__init__()
        self.params = params
        if params is not None:
            self.model = model(**params)
        else:
            self.model = model()

    def transform(self):
        """
        Метод для предварительной обработки данных.
        В этом классе он не реализован.
        """
        raise NotImplementedError("Transform method for ClusteringModel not implemented")

    def fit(self, x_train, start_loc, radius=10):
        """
        Обучение модели.

        Params:
            x_train(2-d array-like) - таблица с признаками объектов.
            start_loc(tuple) - координаты стартовой точки.
        """
        def update_location(loc):
            dx = (start_loc[0] - loc[0])
            dy = (start_loc[1] - loc[1])

            distance = math.sqrt(dx ** 2 + dy ** 2)
            angle = math.atan2(dy, dx)

            new_x = math.cos(angle) * (distance + radius)
            new_y = math.sin(angle) * (distance + radius)
            return [new_x, new_y]

        x_train = [update_location(p) for p in x_train]
        self.x_train = x_train
        self.model.fit(x_train)

    def predict(self):
        """
        Предсказание модели.

        Returns:
            array-like - метки классов.
        """

        return self.model.labels_

    def fit_predict(self, x_train, start_loc, radius=10):
        """
        Обучение и предсказание модели.

        Params:
            x_train(2-d array-like) - таблица с признаками объектов.
            start_loc(tuple) - координаты стартовой точки.
        Returns:
            array-like - метки классов.
        """

        self.fit(x_train, start_loc, radius)
        return self.predict()

