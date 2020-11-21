from data_processing.osm_data_processor import OSMDataProcessor
from optimizer.or_tools_optimizer import ORToolsOptimizer
from utils.classes import Graph
from ml_module.clustering_model import ClusteringModel
from utils.functions import get_points_coordinates_from_query_result, get_matrix_distance


def get_optimal_route(params):
    """
    Построение маршрута.

    Params:
        params(dict) - параметры с ограничениями для маршрута.

    Returns:
        dict - параметры для оптимального маршрута.

    """

    # Эти параметря добавлены в качестве примера. По умолчанию они должны быть доступны в params.
    if params['is_coords']:
        lat, lon = map(float, params['start_loc'].split())
    else:
        lat, lon = 54.7170465, 20.5022674  # TODO: add Nominatim geodecoding
    max_distance = 2000  # TODO convert (start_time, end_time) to distance
    # tags = ['entertainment', 'religion', 'tourism', 'architecture', 'historic']
    tags = [params['trip_type'], 'tourism']  # TODO change tags creation mechanism

    osm_data_processor = OSMDataProcessor()
    query_result = osm_data_processor.get_nearest_points(
        lat=lat,
        lon=lon,
        max_distance=max_distance,
        tags=tags
    )
    nearest_points = get_points_coordinates_from_query_result(query_result)
    clustering_model = ClusteringModel()
    labels = clustering_model.fit_predict(nearest_points)
    matrix_distance = get_matrix_distance(nearest_points)
    graph = Graph(nearest_points)
    or_tools_optimizer = ORToolsOptimizer(graph)
    best_routes = or_tools_optimizer.solve()
    return best_routes

