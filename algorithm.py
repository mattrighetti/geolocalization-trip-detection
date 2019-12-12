from shapely.geometry import Polygon, Point, LineString, shape
from enum import Enum
from haversine import haversine
from geopy import distance

import math
import geopandas as gpd

# TODO Step 0 Parse the GeoJSON.
#       Input: Flask request.args.get()
#       Output: user_route -> List of Point (Shapely class)
user_route = []

# TODO Step 1 Find the first(I) and the last(F) user coordinates.
#       Input: user_route: a list of Point()
#       Output: 2 Point -> I and F

#   Find the first & last user coordinates.
#   params:  - user_route: a list of Point()
#   returns: - the first point of the user route
def find_points(user_route):
    return user_route[0], user_route[len(user_route) - 1]

# TODO Step 2 Find bus stops near I. Do the same for E.
#       Input: I and F
#       Output: 2 list Tuples: Ilist, Flist -> tuple: (bus, stop)
# N.B. User haversine() to see the distance between two Point and compare the value with a threshold



# TODO Step 3 Do the intersection in order to find the bus lines in common.
#       Input: Ilist, Flist
#       Output: Ilist, Flist -> filtered with only the tuples (bus, stop) with bus field in I and E


# TODO Step 4 Create a list of bus routes that have a starting point in Ilist and an end in Flist
#       Input: Ilist, Flist
#       Output: bus_routes -> list of list of Point -> every list of Point represents a bus route


# TODO Step 5 For every route in bus_route compute its metrics.
#
#       metrics: 1) user_coordinates_matched: number of Point in user_route contained in at least
#                                             one polygon of the bus route.
#                2) polygons_matched: number of polygons of the bus route containing at least one
#                                     Point of user_route.
#
#       Input: bus_routes, user_route
#       Output: list of route_dictionary
#                           result_dict = {
#                                               "route" : bus_route,
#                                               "percentage_user": user_metric,
#                                               "number_user_coordinates": len(user_coordinates_matched),
#                                               "percentage_poly": poly_metric,
#                                               "number_polygons": len(polygons_matched)
#                                           }



# TODO Step 6 Search the dictionary with the maximum metrics (TODO Decide a criterion to choose the best one)
#       Input: list of route_dictionary
#       Output: route_dictionary


# TODO Step 7 Calculate the distance with haversine()
#       Input: route_dictionary
#       Output: km_travelled


# TODO Step 8 Save the data in the database
#       Input: user_id, ticket_id, km_travelled

if __name__ == '__main__':

    # STEP 0
    # Parse the GeoJSON.
    user_data = {
        'route': route,
        'user_id': user_id,
        'ticket_id': ticket_id
    }

    # STEP 1
    # Retrieving initial and finhsing Point of user's trip
    initial_point, finishing_point = find_points(mock_route)

    # STEP 2
    # Find bus stops near I. Do the same for E
    from stops import stops
    stops_object = stops()
    Ilist = stops_object.find_bus_stops_close_to(initial_point, radius=5e-3)
    Flist = stops_object.find_bus_stops_close_to(finishing_point, radius=5e-3)

    # STEP 3
    # Do the intersection in order to find the bus lines in common
    Ilist, Flist = stops.intercept(Ilist, Flist)

    # STEP 4
    # Create a list of bus routes that have a starting point in Ilist and an end in Flist
    from linestring_selector import LinestringSelector
    linestring_selector = LinestringSelector(Ilist, Flist)
    sliced_routes = linestring_selector.get_sliced_routes()

    # STEP 5
    # For every route in bus_route compute its metrics.
    route_dictionaries = None

    # STEP 6
    # Search the dictionary with the maximum metrics
    from metrics_evaluator import metrics_evaluator
    evaluator = metrics_evaluator(route_dictionaries)
    best_route = evaluator.evaluate()

    # STEP 7
    # Calculate the distance with haversine
    km_travelled = 0

    # STEP 8
    # Save the data in the database
    # TODO change API endpoint
    from post_request import save_to_database
    save_to_database(user_data['user_id'], user_data['ticket_id'], km_travelled)