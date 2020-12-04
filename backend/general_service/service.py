import time

from optimal_route.optimizer import Optimizer

from utils.configuration import service, TRIP_TYPES_MAPPING


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
        speed = 66  # meters in minute
        start_params = {'start_lat': params.get('start_lat', type=float),
                        'start_lng': params.get('start_lng', type=float),
                        'distance': time_for_route * speed,
                        'tags': ['historic', 'food', 'pharmacy']}
        max_points = int(25 * time_for_route / 60)
        print("Max points:", max_points, flush=True)
        # TODO считывать trip_type и дополнительные типы точек типа аптек и ресторанов
        # trip_type = params.get('trip_type', type=str)
        # start_params['tags'] = service[TRIP_TYPES_MAPPING][trip_type]

        # osm_data_processor = OSMDataProcessor()
        # query_result = osm_data_processor.get_nearest_points(
        #     lat=lat,
        #     lon=lng,
        #     max_distance=distance,
        #     tags=service[TRIP_TYPES_MAPPING][trip_type],
        # )
        # nearest_points = get_points_coordinates_from_query_result(query_result)
        # clustering_model = ClusteringModel()
        # labels = clustering_model.fit_predict(nearest_points)
        # constructor = OsmGraphConstructor(osm_data_processor, "./cache/", cache=False)
        graph = self.constructor.create_graph(start_params, max_points=max_points)

        need_return = False

        opt = Optimizer(speed=speed)
        route = opt.solve(graph.data, time_for_route, need_return=need_return)

        return graph.get_way(route)
