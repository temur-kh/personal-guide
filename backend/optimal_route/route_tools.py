# -*- coding: utf-8 -*-
import math
import time
import numpy as np
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from ortools.sat.python import cp_model


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


def calc_route_distance(route, distance_matrix):
    nv = len(route) - 1
    total_len = 0
    for iv in range(nv):
        jv = iv + 1
        # get path between iv and jv
        i_id_in_map = route[iv]
        j_id_in_map = route[jv]
        if j_id_in_map == i_id_in_map:
            continue
        len_path = distance_matrix[i_id_in_map][j_id_in_map]
        total_len += len_path
    return total_len


def limit_route(data, route, max_distance, need_return, distance_matrix):
    nv = len(route) - 1
    cur_len = 0
    limited_route = [route[0]]
    back_path = 0
    starting_point = data['depot']
    for iv in range(nv):
        jv = iv + 1
        i_id_in_map = route[iv]
        j_id_in_map = route[jv]
        if j_id_in_map == i_id_in_map:
            continue
        len_path = distance_matrix[i_id_in_map][j_id_in_map]
        cur_len += len_path
        limited_route.append(route[jv])
        if need_return:
            back_path = distance_matrix[j_id_in_map][starting_point]
        if cur_len + back_path >= max_distance:
            limited_route.append(starting_point)
            break
    return limited_route, cur_len + back_path


def find_route_with_distance_limit(data, distance_matrix, max_distance, need_return, hard=False):
    route = find_ortools_route_with_distance_matrix(data, distance_matrix, hard=hard)
    total_distance = calc_route_distance(route, distance_matrix)
    if total_distance < max_distance * 1.1:
        return route

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

        limited_route, route_distance = limit_route(data, route, max_distance, need_return, distance_matrix)

        routes.append(limited_route)
        distances.append(route_distance)
        num_nodes.append(len(limited_route) - 1)
        print('Route {} with {} nodes, distance {}'.format(strategy, len(limited_route) - 1, route_distance))

    max_route_ids = np.argwhere(num_nodes == np.amax(num_nodes)).flatten().tolist()
    distances = np.array(distances)[max_route_ids]
    min_dist_id = np.argmin(distances)
    return routes[max_route_ids[min_dist_id]]


class SolutionWithLimit(cp_model.CpSolverSolutionCallback):
    def __init__(self, limit, deadline_seconds):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0
        self.__solution_limit = limit
        self.__deadline_sec = deadline_seconds
        self.__time_run = time.time()

    def on_solution_callback(self):
        self.__solution_count += 1
        if (time.time() - self.__time_run) > self.__deadline_sec \
                or self.__solution_count >= self.__solution_limit:
            print('Stop search after %i solutions' % self.__solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count


def reward_collecting_tsp(data, max_distance, stop_dists=None):
    """
    data(dict) - информациея о poi. Ключи:
                ids(list) - список id_osm.
                category(list) - список категорий poi.
                locations(list) - список координат poi в формате: [lat, lon].
                nv(int) - кол-во poi.
                num_vehicles(int)
                depot(int) - индекс(в ids) стартовой точки.
                constraints(dict) - словарь constraints с индексами(в ids):
                        {category_constraint: [], ...}
                distance_matrix(list) - матрица кратчайших расстояний(int), размером (nv, nv)
                rewards(list) - список наград для точек интереса.
                stop_time(list) - список врмени остановки на poi.
    """
    print("Total number of points:", len(data['rewards']), flush=True)
    print("All rewards:", data['rewards'], flush=True)

    num_nodes = data['nv']
    visit_rewards = data['rewards']
    distance_matrix = data['distance_matrix']

    all_nodes = range(num_nodes)
    model = cp_model.CpModel()

    obj_vars = []
    obj_coeffs = []
    lits = []
    dists = []
    stops = []
    route = []
    visited_nodes = []
    arc_literals = {}

    # Create the circuit constraint.
    arcs = []
    for i in all_nodes:
        is_visited = model.NewBoolVar('%i is visited' % i)
        arcs.append([i, i, is_visited.Not()])

        obj_vars.append(is_visited)
        obj_coeffs.append(visit_rewards[i])

        visited_nodes.append(is_visited)

        for j in all_nodes:
            if i == j:
                continue

            lit = model.NewBoolVar('%i follows %i' % (j, i))
            arcs.append([i, j, lit])
            arc_literals[i, j] = lit

            lits.append(lit)
            dists.append(int(distance_matrix[i][j]))
            if stop_dists:
                stops.append(stop_dists[j])

    model.AddCircuit(arcs)

    starting_point = data['depot']
    model.Add(visited_nodes[starting_point] == 1)

    for constraint, idxs in data['constraints'].items():
        model.Add(sum(visited_nodes[i] for i in idxs) == 1)

    # The maximal distance of a route should not exceed max_distance

    if stop_dists:
        model.Add(sum(lits[i] * (dists[i] + stops[i]) for i in range(len(lits))) <= max_distance)
    else:
        model.Add(sum(lits[i] * dists[i] for i in range(len(lits))) <= max_distance)

    # Maximize reward from visited nodes.
    model.Maximize(
        sum(obj_vars[i] * obj_coeffs[i] for i in range(len(obj_vars))))

    # Solve and print out the solution.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120
    solver.parameters.log_search_progress = True
    # To benefit from the linearization of the circuit constraint.
    solver.parameters.linearization_level = 2

    # находит первое решение и возвращает его
    solution_printer = SolutionWithLimit(limit=10, deadline_seconds=8)
    solverStatus = solver.SolveWithSolutionCallback(model, solution_printer)
    if solverStatus == 3: #INFEASIBLE
        return [], 0
    # solver.Solve(model)

    print(solver.ResponseStats())

    first_visited_node = starting_point

    if first_visited_node != -1:
        current_node = first_visited_node
        str_route = '%i' % current_node
        route.append(current_node)
        route_is_finished = False
        route_distance = 0
        value_collected = 0
        while not route_is_finished:
            value_collected += visit_rewards[current_node]
            for i in all_nodes:
                if i == current_node:
                    continue
                if solver.BooleanValue(arc_literals[current_node, i]):
                    str_route += ' -> %i' % i
                    route.append(i)
                    route_distance += distance_matrix[current_node][i]
                    current_node = i
                    if current_node == first_visited_node:
                        route_is_finished = True
                    break

        print('Route:', str_route)
        print('Travelled distance:', route_distance)
        print('Value collected: ', value_collected)

    return route, route_distance
