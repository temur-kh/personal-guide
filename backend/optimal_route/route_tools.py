# -*- coding: utf-8 -*-
import math
import numpy as np
# from ortools.graph import pywrapgraph
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = (int(
                    math.hypot((from_node[0] - to_node[0]),
                               (from_node[1] - to_node[1]))))
    return distances


def fill_distance_matrix(data, paths):
    nv = data['nv']
    data['distance_matrix'] = np.zeros((nv, nv))
    distances = {}  # alternative place to store distances
    for iv in range(nv):
        distances[iv] = {}
        i_id_in_map = data['ids'][iv]
        for jv in range(nv):
            j_id_in_map = data['ids'][jv]
            if iv == jv or j_id_in_map == i_id_in_map:
                distances[iv][jv] = 0
                continue

            path = paths[i_id_in_map][j_id_in_map]
            data['distance_matrix'][iv][jv] = path.get_distance()
            distances[iv][jv] = path.get_distance()
    return distances


def test_ortools(data, distances=False, hard=False):
    """Entry point of the program."""
    # Instantiate the data problem.
    print('Start routing ... ')
    if distances:
        # data = dt.create_data_model_distance()

        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['depot'])

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
    else:
        # data = dt.create_data_model_locations()

        manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                               data['num_vehicles'], data['depot'])

        distance_matrix = compute_euclidean_distance_matrix(data['locations'])

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    if hard:
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = 2
        search_parameters.log_search = True
    else:
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    routes = get_routes(solution, routing, manager)
    # Display the routes.
    for i, route in enumerate(routes):
        print('Route', i, route)

    return routes[0]


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def find_ortools_route_with_distance_matrix(data, distance_matrix, hard=False, strategy=None):
    """Entry point of the program."""
    # Instantiate the data problem.
    print('Start routing ... ')

    manager = pywrapcp.RoutingIndexManager(data['nv'],
                                           data['num_vehicles'], data['depot'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    if hard:
        if strategy is None:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        else:
            search_parameters.local_search_metaheuristic = (strategy)

        search_parameters.time_limit.seconds = 1
        # search_parameters.log_search = True
    else:
        if strategy is None:
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
        else:
            search_parameters.first_solution_strategy = (strategy)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    routes = get_routes(solution, routing, manager)
    # Display the routes.
    for i, route in enumerate(routes):
        print('Route', i, route)

    return routes[0]


def calc_route_distance(data, route, paths):
    nv = len(route) - 1
    total_len = 0
    for iv in range(nv):
        jv = iv + 1
        # get path between iv and jv
        i_id_in_map = data['ids'][route[iv]]
        j_id_in_map = data['ids'][route[jv]]
        if j_id_in_map == i_id_in_map:
            continue
        len_path = paths[i_id_in_map][j_id_in_map].get_distance()
        total_len += len_path
    return total_len


def limit_route(data, route, max_distance, need_return, paths):
    nv = len(route) - 1
    cur_len = 0
    limited_route = [route[0]]
    back_path = 0
    starting_point = data['depot']
    starting_point_in_map = data['ids'][starting_point]
    for iv in range(nv):
        jv = iv + 1
        i_id_in_map = data['ids'][route[iv]]
        j_id_in_map = data['ids'][route[jv]]
        if j_id_in_map == i_id_in_map:
            continue
        len_path = paths[i_id_in_map][j_id_in_map].get_distance()
        cur_len += len_path
        limited_route.append(route[jv])
        if need_return:
            back_path = paths[j_id_in_map][starting_point_in_map].get_distance()
        if cur_len + back_path >= max_distance:
            limited_route.append(starting_point)
            break
    return limited_route, cur_len + back_path


def find_route_with_distance_limit(data, distance_matrix, max_distance, paths, need_return, hard=False):
    route = find_ortools_route_with_distance_matrix(data, distance_matrix, hard=hard)
    total_distance = calc_route_distance(data, route, paths)
    if total_distance < max_distance * 1.1:
        return route
    # if not need_return:
    #    return limit_route(data, route, max_distance, paths)

    firstSearchStrategies = [
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC,
        ##routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC,
        ##routing_enums_pb2.FirstSolutionStrategy.EVALUATOR_STRATEGY,
        # routing_enums_pb2.FirstSolutionStrategy.SAVINGS,
        # routing_enums_pb2.FirstSolutionStrategy.SWEEP,
        # routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES,
        # routing_enums_pb2.FirstSolutionStrategy.BEST_INSERTION,
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
        routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION,
        routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC,
        routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC
    ]
    '''
    localSearchStrategies = [
        routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT,
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH,
        routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING,
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH,
        #routing_enums_pb2.LocalSearchMetaheuristic.OBJECTIVE_TABU_SEARCH
    ]
    '''
    routes = []
    num_nodes = []
    distances = []
    for strategy in firstSearchStrategies:
        route = find_ortools_route_with_distance_matrix(data, distance_matrix,
                                                        hard=False, strategy=strategy)
        limited_route, route_distance = limit_route(data, route, max_distance, need_return, paths)
        routes.append(limited_route)
        distances.append(route_distance)
        num_nodes.append(len(limited_route) - 1)
        print('Route {} with {} nodes, distance {}'.format(strategy, len(limited_route) - 1, route_distance))

    max_route_ids = np.argwhere(num_nodes == np.amax(num_nodes)).flatten().tolist()
    distances = np.array(distances)[max_route_ids]
    min_dist_id = np.argmin(distances)
    return routes[max_route_ids[min_dist_id]]