import numpy as np
import geopandas as gpd
from shapely.geometry import LineString, Point

# INPUT
# List of NP.ARRAYs with data

class LinestringSelector(object):
    def __init__(self, Istops, Fstops):
        self.data = gpd.read_file("./data/bus routes.geojson")
        self.Istops = Istops
        self.Fstops = Fstops

    def _get_routes_to_analyse(self):
        # TODO pick number of bus for each stop and get their routes
        print("Do it")

    def _convert_to_multilinestring(self, linestring):
        linestring_array = []

        for i in range(len(linestring.coords) - 1):
            tuple_1 = linestring.coords[i]
            tuple_2 = linestring.coords[i + 1]
            first_point = Point(tuple_1)
            second_point = Point(tuple_2)
            linestring_new = LineString([first_point, second_point])
            linestring_array.append(linestring_new)

        return np.asarray(linestring_array, dtype=LineString)


    def _get_sliced_multi_linestring(self, linestring, starting_point, finishing_point):
        multi_linestring = self._slice_to_multilinestring(linestring)
        starting_index = self._get_index_of_min_distance(multi_linestring, starting_point)
        finishing_index = self._get_index_of_min_distance(multi_linestring, finishing_point)

        # TODO check index order to apply logic (if starting comes latter than finishing then do logic)
        if starting_index < finishing_index:
            sliced_multi_linestring = multi_linestring[starting_index:finishing_index]
        elif finishing_index < starting_index:
            # TODO check a scenario to see what could be done
            raise Exception("Not yet implemented")
        else:
            # TODO can they be equal? Should not be
            return np.array([])

    def _convert_to_linestring(self, multi_linestring):
        return LineString(multi_linestring)

    def _get_index_of_min_distance(self, multi_linestring, point):
        distances = []

        for linestring in multi_linestring:
            dist = linestring.distance(point)
            distances.append(dist)

        return distances.index(min(distances))