from optimal_route import osmp_tools as ost
from optimal_route.optimizer import Optimizer


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
    speed = 100  # meters in minute
    ost.set_start_coords(lat, lng)
    ost.set_map_distance(time_for_route * speed)
    points_of_interest = ost.get_berlin_cafes()
    need_return = False

    opt = Optimizer(speed=speed)
    route, paths = opt.solve((lat, lng), points_of_interest, time_for_route, need_return=need_return)

    return get_path(points_of_interest, opt.og, route, paths)


def get_path(data, og, route, paths):
    result_paths = []
    points = []
    total_points = len(route) - 1
    for index in range(total_points):
        next_index = index + 1
        index_in_map = data['ids'][route[index]]
        next_index_in_map = data['ids'][route[next_index]]
        points.append({"lng": og.pos[index_in_map][0], "lat": og.pos[index_in_map][1]})

        path = paths[index_in_map][next_index_in_map].get_path()
        for point in path:
            result_paths.append({"lng": og.pos[point][0], "lat": og.pos[point][1]})

    index_in_map = data['ids'][route[total_points]]
    points.append({"lng": og.pos[index_in_map][0], "lat": og.pos[index_in_map][1]})
    return points, result_paths
