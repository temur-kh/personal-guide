from data_processing.osm_data_processor import OSMDataProcessor
from optimizer.or_tools_optimizer import ORToolsOptimizer
from utils.classes import Graph
from ml_module.clustering_model import ClusteringModel


def get_optimal_route(params):
    """
    Построение маршрута.

    Params:
        params(dict) - параметры с ограничениями для маршрута.

    Returns:
        dict - параметры для оптимального маршрута.

    """

    osm_data_processor = OSMDataProcessor('osm')
    points_for_route = osm_data_processor.query()
    graph = Graph(points_for_route)
    or_tools_optimizer = ORToolsOptimizer(graph)
    tmp_routes = or_tools_optimizer.solve()
    clustering_model = ClusteringModel()
    best_routes = clustering_model.fit_predict(tmp_routes)
    return best_routes

