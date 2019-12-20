from geopy import distance
from Utils.database_manager import MongoDBManager
from Utils.stops import stops, intercept
from Utils.linestring_selector import LinestringSelector
from Utils.routes_analyzer import routes_analyzer
from Utils.metrics_evaluator import metrics_evaluator
from Utils.NetworkManager import send_data



# Step 0 Parse the GeoJSON.
#       Input: Flask request.args.get()
#       Output: user_route -> List of Point (Shapely class)

# Step 1 Find the first(I) and the last(F) user coordinates.
#       Input: user_route: a list of Point()
#       Output: 2 Point -> I and F

# Step 2 Find bus stops near I. Do the same for E.
#       Input: I and F
#       Output: 2 list Tuples: Ilist, Flist -> tuple: (bus, stop)
# N.B. User haversine() to see the distance between two Point and compare the value with a threshold



# Step 3 Do the intersection in order to find the bus lines in common.
#       Input: Ilist, Flist
#       Output: Ilist, Flist -> filtered with only the tuples (bus, stop) with bus field in I and E


# Step 4 Create a list of bus routes that have a starting point in Ilist and an end in Flist
#       Input: Ilist, Flist
#       Output: bus_routes -> list of list of Point -> every list of Point represents a bus route


# Step 5 For every route in bus_route compute its metrics.
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



# Step 6 Search the dictionary with the maximum metrics
#       Input: list of route_dictionary
#       Output: route_dictionary


# Step 7 Calculate the distance with haversine()
#       Input: route_dictionary
#       Output: km_travelled

# Step 8 Save the data in the database
#       Input: user_id, ticket_id, km_travelled



def detect_vehicle_and_km(user_route: list, app=None):

    # STEP 1
    # Retrieving initial and finhsing Point of user's trip
    initial_point, finishing_point = find_points(user_route)
    if app is not None:
        app.logger.info("Found initial and finishing point")

    # STEP 2
    # Find bus stops near I. Do the same for E
    stops_object = stops()
    offset_square = 0.001
    Ilist = stops_object.find_bus_stops_close_to(initial_point, radius=offset_square)
    Flist = stops_object.find_bus_stops_close_to(finishing_point, radius=offset_square)
    if app is not None:
        app.logger.info("Inital bus stops: %d", len(Ilist))
        app.logger.info("Finishing bus stops: %d", len(Flist))

    # STEP 3
    # Do the intersection in order to find the bus lines in common
    Ilist, Flist = intercept(Ilist, Flist)
    if app is not None:
        app.logger.info("Bus stops interception: %d", len(Ilist))


    # STEP 4
    # Create a list of bus routes that have a starting point in Ilist and an end in Flist
    linestring_selector = LinestringSelector(Ilist, Flist)
    sliced_routes = linestring_selector.get_sliced_routes()
    if app is not None:
        app.logger.info("Bus routes found: %d", len(sliced_routes))


    # STEP 5
    # For every route in bus_route compute its metrics.
    analyzer = routes_analyzer(sliced_routes, user_route)
    route_dictionaries = analyzer.compute_metrics()

    # STEP 6
    # Search the dictionary with the maximum metrics
    evaluator = metrics_evaluator(route_dictionaries)
    best_route = evaluator.evaluate()
    if app is not None:
        app.logger.info("Metrics: {")
        app.logger.info("\tpercentage_user: %f", best_route['percentage_user'])
        app.logger.info("\tnumber_user_coordinates: %d", best_route['number_user_coordinates'])
        app.logger.info("\tpercentage_poly: %f", best_route['percentage_poly'])
        app.logger.info("\tnumber_polygons: %d", best_route['number_polygons'])
        app.logger.info("}")

    # STEP 7
    # Calculate the distance with haversine
    km_travelled = compute_kilometers(best_route['route'])
    if app is not None:
        app.logger.info("km calculated: %f", km_travelled)
    vehicle = "bus"
    return vehicle, km_travelled


#   Find the first & last user coordinates.
#   params:  - user_route: a list of Point()
#   returns: - the first point of the user route
def find_points(user_route):
    return user_route[0], user_route[len(user_route) - 1]


#Given a route (list of Point) returns the kilometers of that route
def compute_kilometers(route: list):
    total_km = 0
    route_length = len(route)

    for point in range(route_length - 1):
        p1 = route[point]
        p2 = route[point + 1]
        p1 = (p1.y,p1.x)
        p2 = (p2.y, p2.x)
        total_km += distance.geodesic(p1, p2, ellipsoid='Intl 1924').km
    
    return total_km


def elaborate_request(user_id, ticket_id, start_time, end_time, data, app=None):
    
    # STEP 0
    # Parse the GeoJSON.
    user_data = {
        'user_id' : user_id,
        'ticket_id' : ticket_id,
        'km_travelled' : None,
        'transportation' : None,
        'start_time' : start_time,
        'end_time' : end_time
        }

    # STEP 1-7
        
    
    vehicle, km_travelled = detect_vehicle_and_km(user_route=data, app=app)

    user_data['km_travelled'] = km_travelled
    user_data['transportation'] = vehicle

    # STEP 8
    # Save the data in the database
    # database_manager = MongoDBManager()
    # database_manager.save_to_database_dict(user_data)

    return user_data