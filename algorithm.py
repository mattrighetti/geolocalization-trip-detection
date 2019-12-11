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

#   Find the first user coordinates.
#   params:  - user_route: a list of Point()
#   returns: - the first point of the user route
def find_first(user_route):
    return user_route[0]

#   Find the last user coordinates.
#   params:  - user_route: a list of Point()
#   returns: - the last point of the user route
def find_last(user_route):
    return user_route[len(user_route) - 1]

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
