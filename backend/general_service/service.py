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
    lat = 54.7170465
    lon = 20.5022674
    max_distance = 2000
    tags = ['entertainment', 'religion', 'tourism', 'architecture', 'historic']

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
    tmp_routes = or_tools_optimizer.solve()
    clustering_model = ClusteringModel()
    best_routes = clustering_model.fit_predict(tmp_routes)
    return best_routes

