from data_processing.osm_data_processor import OSMDataProcessor
from graph_constructor.osm_graph_constructor import OsmGraphConstructor
from optimal_route.optimizer import Optimizer

from utils.configuration import service, TRIP_TYPES_MAPPING


def get_optimal_route(params):
    """
    Построение маршрута.

    Params:
        params(dict) - параметры с ограничениями для маршрута.

    Returns:
        dict - параметры для оптимального маршрута.

    """
    time_for_route = params.get('duration', type=int)  # minutes
    lat = params.get('start_lat', type=float)
    lng = params.get('start_lng', type=float)
    trip_type = params.get('trip_type', type=str)
    speed = 100  # meters in minute
    distance = time_for_route * speed

    osm_data_processor = OSMDataProcessor()
    # query_result = osm_data_processor.get_nearest_points(
    #     lat=lat,
    #     lon=lng,
    #     max_distance=distance,
    #     tags=service[TRIP_TYPES_MAPPING][trip_type],
    # )
    # nearest_points = get_points_coordinates_from_query_result(query_result)
    # clustering_model = ClusteringModel()
    # labels = clustering_model.fit_predict(nearest_points)
    constructor = OsmGraphConstructor(osm_data_processor, "./cache/", cache=False)
    graph = constructor.create_graph(
        lat,
        lng,
        distance,
        tags=service[TRIP_TYPES_MAPPING][trip_type],
    )
    need_return = False

    opt = Optimizer(speed=speed)
    route = opt.solve(graph.data, time_for_route, need_return=need_return)

    return get_path(graph, route)


def get_path(og, route):
    result_paths = []
    points = []
    for index in route:
        points.append({"lng": og.data['locations'][index][1], "lat": og.data['locations'][index][0]})
    for line in og.get_way(route):
        result_paths.append({"lng": line[1], "lat": line[0]})
    return points, result_paths
