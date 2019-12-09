from shapely.geometry import Point, Polygon

class routes_analyzer(object):

    def __init__(self, bus_routes: list, user_route: list):
        self.bus_routes = bus_routes
        self.user_route = self._remove_duplicates(user_route)

    def compute_metrics(self):
        dictionaries = []

        for route in self.bus_routes:

            # TODO can we do it before?
            route = self._remove_duplicates(route)

            result_dict = self._compute_route_metrics(route)
            dictionaries.append(result_dict)
        
        return dictionaries

    def _create_polygons(self, bus_route:list):
        polygons = []

        for coordinate in range(len(bus_route) - 1):
            p1 = Point(bus_route[coordinate].x,bus_route[coordinate].y)
            p2 = Point(bus_route[coordinate + 1].x,bus_route[coordinate + 1].y)

            assert p1.x != p2.x
            assert p1.y != p2.y

            v1,v2,v3,v4 = self._create_polygon_vertices(p1,p2)
            polygon = Polygon([v1,v2,v4,v3])
            polygons.append(polygon)
        
        return polygons
    
    # Analyze a single route
    def _compute_route_metrics(self, bus_route:list):
        bus_route_polygons = self._create_polygons(bus_route)
        user_coordinates_matched = []
        polygons_matched = []

        for point in self.user_route:
            for poly in bus_route_polygons:
                if poly.contains(point):
                    if point not in user_coordinates_matched:
                        user_coordinates_matched.append(point)
                    if poly not in polygons_matched:
                        polygons_matched.append(poly)
        
        user_metric = len(user_coordinates_matched) / len(self.user_route)
        poly_metric = len(polygons_matched)/ len(bus_route_polygons)

        result_dict = { 
                    "route" : bus_route, 
                    "number_user_coordinates": len(user_coordinates_matched), 
                    "number_polygons": len(polygons_matched),
                    "percentage_user": user_metric,
                    "percentage_poly": poly_metric
                }

        return result_dict

    # Create the vertices of a polygon given two points of the route
    def _create_polygon_vertices(self, first_p: Point, second_p: Point):

        offset_small_x = 0.00020810000000004436
        offset_small_y = 0.00015400000000198588
        offset_x = 0.0004000000000008441
        offset_y = 0.0002460000000041873

        #find perpendicular sine and cosine
        cosine = - (second_p.y - first_p.y) / second_p.distance(first_p)
        sine = - (second_p.x - first_p.x) / second_p.distance(first_p)

        #Add the small offset (use the normal sine and cosine, not the perpendicular just found)
        first_p_with_small_offset = Point( (first_p.x - first_p.x*sine), (first_p.y - first_p.y*cosine))
        second_p_with_small_offset = Point( (second_p.x + second_p.x*sine), (second_p.y + second_p.y*cosine))
        
        dx = offset_x * cosine
        dy = offset_y * sine
        
        if dx < offset_small_x:
            dx = offset_small_x
        if dy < offset_small_y:
            dy = offset_small_y
        
        new_p1 = (first_p_with_small_offset.x-dx, first_p_with_small_offset.y-dy)
        new_p2 = (second_p_with_small_offset.x-dx, second_p_with_small_offset.y-dy)
        new_p3 = (first_p_with_small_offset.x+dx, first_p_with_small_offset.y+dy)
        new_p4 = (second_p_with_small_offset.x+dx, second_p_with_small_offset.y+dy)
        
        return new_p1, new_p2, new_p3, new_p4
    
    def _remove_duplicates(self, points: list):
        unique_list = []

        for point in points:
            if point not in unique_list:
                unique_list.append(point)
        
        return unique_list