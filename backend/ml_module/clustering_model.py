from sklearn.cluster import KMeans

from backend.ml_module.base_ml_model import MLModel


class ClusteringModel(MLModel):
    """
    Класс для кластеризации точек на карте.

    Attributes:
        model(sklearn.cluster) - модель для кластеризации.
        n_clusters(int) - число кластеров, если в модели есть такой параметр, иначе None.
        x_train(2-d array-like) - таблица с признаками объектов.
    """
    model = None
    n_clusters = None

    def __init__(self, model=KMeans, n_clusters=None):
        """
        Создание модели для кластеризации

        Params:
            model(sklearn.cluster) - модель для кластеризации.
            n_clusters(int) - число кластеров, если в модели есть такой параметр, иначе None.
        """

        super().__init__()
        self.n_clusters = n_clusters
        if n_clusters is not None:
            self.model = model(n_clusters)
        else:
            self.model = model()

    def transform(self):
        """
        Метод для предварительной обработки данных.
        В этом классе он не реализован.
        """
        raise NotImplementedError("Transform method for ClusteringModel not implemented")

    def fit(self, x_train):
        """
        Обучение модели.

        Params:
            x_train(2-d array-like) - таблица с признаками объектов.
        """

        self.x_train = x_train
        self.model.fit(x_train)

    def predict(self):
        """
        Предсказание модели.

        Returns:
            array-like - метки классов.
        """

        return self.model.labels_

    def fit_predict(self, x_train):
        """
        Обучение и предсказание модели.

        Params:
            x_train(2-d array-like) - таблица с признаками объектов.

        Returns:
            array-like - метки классов.
        """

        self.fit(x_train)
        return self.predict()

