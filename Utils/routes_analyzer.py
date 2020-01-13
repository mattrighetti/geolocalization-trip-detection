from shapely.geometry import Point, Polygon

class routes_analyzer(object):

    def __init__(self, routes: list, user_route: list):
        self.vehicle_routes = routes
        self.user_route = self._remove_duplicates(user_route)
        # self.user_route = user_route

    def compute_metrics(self):
        dictionaries = []

        self.check_input_corretness()

        # Compute metrics for each bus route and append to a list
        for route in self.vehicle_routes:
            # Remove duplicate points from the list and reconstruct the tuple
            route = (self._remove_duplicates(route[0]), route[1])
            # Compute metrics for each bus route
            result_dict = self._compute_route_metrics(route)
            dictionaries.append(result_dict)

        return dictionaries

    # Check if all the data structures are the one expected by the class
    def check_input_corretness(self):
        # Check that the bus routes list is not empty
        if (len(self.vehicle_routes) == 0):
            raise Exception('Bus routes is empty')
        
        # Check that bus routes is a list
        if (not isinstance(self.vehicle_routes, list)):
            raise Exception('Bus routes is not a list but ' + str(type(self.vehicle_routes)))

        # Check that the list contains Point
        if (not isinstance(self.vehicle_routes[0][0][0], Point)):
            raise Exception('Bus routes does not contain Points but ' + str(type(self.vehicle_routes[0][0][0])))

    # Given a list of Point representing the bus route return a list of Polygon 
    def _create_polygons(self, route: list):
        polygons = []


        for coordinate in range(len(route) - 1):
            p1 = Point(route[coordinate].x,
                       route[coordinate].y)
            p2 = Point(route[coordinate + 1].x,
                       route[coordinate + 1].y)
            assert p1.x != p2.x or p1.y != p2.y

            v1, v2, v3, v4 = self._create_polygon_vertices(p1, p2)
            polygon = Polygon([v1, v2, v4, v3])
            polygons.append(polygon)

        return polygons

    # Analyze a single route
    def _compute_route_metrics(self, route: tuple):
        #Create the polygons with the route, store in the first position of the tuple (List of Point, 'VECHICLE')
        bus_route_polygons = self._create_polygons(route[0])
        user_coordinates_matched = []
        polygons_matched = []

        # For every Point in the user route
        for point in self.user_route:
            # For every Polygon in the bus route
            for poly in bus_route_polygons:
                # If the Polygon contanins the Point
                if poly.contains(point):
                    # If the Point and the Polygon are not already matched add them to their data structure 
                    if point not in user_coordinates_matched:
                        user_coordinates_matched.append(point)
                    if poly not in polygons_matched:
                        polygons_matched.append(poly)

        # Compute the metrics
        
        user_metric = 0
        if len(bus_route_polygons) > 0:
            user_metric = len(user_coordinates_matched) / len(self.user_route)
        
        poly_metric = 0
        if len(bus_route_polygons) > 0:
            poly_metric = len(polygons_matched) / len(bus_route_polygons)

        result_dict = { 
                    'route' : route[0], 
                    'vehicle': route[1],
                    'percentage_user': user_metric,
                    'number_user_coordinates': len(user_coordinates_matched), 
                    'percentage_poly': poly_metric,
                    'number_polygons': len(polygons_matched)
                }

        return result_dict

    # Create the vertices of a polygon given two points of the route
    def _create_polygon_vertices(self, first_p: Point, second_p: Point):

        offset_small_x = 9.999999999976694e-05
        offset_small_y = 5.000000000165983e-05
        offset_x = 0.0001499999999996504
        offset_y = 0.00013599999999769352

        # find perpendicular sine and cosine
        cosine = - (second_p.y - first_p.y) / second_p.distance(first_p)
        sine = - (second_p.x - first_p.x) / second_p.distance(first_p)

        # Add the small offset (use the normal sine and cosine, not the perpendicular just found)
        first_p_with_small_offset = Point(
            (first_p.x - first_p.x*sine), (first_p.y - first_p.y*cosine))
        second_p_with_small_offset = Point(
            (second_p.x + second_p.x*sine), (second_p.y + second_p.y*cosine))

        dx = offset_x * cosine
        dy = offset_y * sine

        # Avoid Polygon dimension from being too small
        if dx < offset_small_x:
            dx = offset_small_x
        if dy < offset_small_y:
            dy = offset_small_y

        new_p1 = (first_p_with_small_offset.x-dx,
                  first_p_with_small_offset.y-dy)
        new_p2 = (second_p_with_small_offset.x-dx,
                  second_p_with_small_offset.y-dy)
        new_p3 = (first_p_with_small_offset.x+dx,
                  first_p_with_small_offset.y+dy)
        new_p4 = (second_p_with_small_offset.x+dx,
                  second_p_with_small_offset.y+dy)

        return new_p1, new_p2, new_p3, new_p4

    def _remove_duplicates(self, points: list):
        unique_list = []
        for point in points:
            if point not in unique_list:
                unique_list.append(point)

        return unique_list
