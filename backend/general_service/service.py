import time
from math import ceil, sqrt

from sklearn.cluster._agglomerative import AgglomerativeClustering

from ml_module.clustering_model import ClusteringModel
from optimal_route.optimizer import Optimizer


class Service():
    def __init__(self, constructor):
        self.constructor = constructor

    def get_optimal_route(self, params):
        """
        Построение маршрута.

        Params:
            params(dict) - параметры с ограничениями для маршрута.

        Returns:
            dict - параметры для оптимального маршрута.

        """
        time_for_route = params.get('duration', type=int)  # minutes
        tags = params.get('tags').split(',')
        constraints = params.get('constraints').split(',')
        speed = 66  # meters in minute

        start_params = {'start_lat': params.get('start_lat', type=float),
                        'start_lng': params.get('start_lng', type=float),
                        'duration': time_for_route,
                        'speed': speed,
                        'distance': time_for_route * speed,
                        'tags': tags + constraints}
        need_return = True if params.get('need_return') == 'true' else False
        max_points = int(25 * time_for_route / 60)
        print("Max points:", max_points, flush=True)

        graph = self.constructor.create_graph(start_params, max_points=max_points)
        point_locations = graph.data['locations']
        start_location = (start_params['start_lat'], start_params['start_lng'])

        n_clusters = max(1, round(len(point_locations) / 75))
        radius = 20  # с потолка
        print("Total number of points:", len(point_locations), flush=True)
        print("Number of clusters:", n_clusters, flush=True)
        clustering_model = ClusteringModel(params={'n_clusters': n_clusters})
        labels = clustering_model.fit_predict(point_locations, start_location, radius=radius)
        clusters = self._labels_to_clusters(labels, n_clusters)
        for i, cluster in enumerate(clusters):
            print(f"Cluster #{i} size:", len(cluster), flush=True)

        opt = Optimizer(speed=speed)
        routes = opt.solve_parallel(graph.data, clusters, time_for_route, need_return)
        res = [graph.get_way(route) for route in routes]
        return res

    def _labels_to_clusters(self, labels, n_clusters):
        clusters = [[] for _ in range(n_clusters)]
        for idx, label in enumerate(labels):
            clusters[label].append(idx)
        return clusters
