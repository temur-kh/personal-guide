# -*- coding: utf-8 -*-
import numpy as np

import time
from ortools.linear_solver import pywraplp
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import data as dt
import route_tools as rt
import osmp_tools as ost

def test_ortools(data, DISTANCES=False, hard=False):
    """Entry point of the program."""
    # Instantiate the data problem.
    print('Start routing ... ')
    if DISTANCES:
        data = dt.create_data_model_distance()
    
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
        
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
    else:
        #data = dt.create_data_model_locations()
        
        manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])
        
        distance_matrix = rt.compute_euclidean_distance_matrix(data['locations'])
        
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
    Strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    if hard:
       Strategy = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (Strategy)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
        
    routes = rt.get_routes(solution, routing, manager)
# Display the routes.
    for i, route in enumerate(routes):
        print('Route', i, route)


if __name__ == '__main__':
    cafes = ost.get_berlin_cafes()
    start = time.time()
    test_ortools(cafes, )
    end = time.time()
    print('Time is {}'.format(end - start))