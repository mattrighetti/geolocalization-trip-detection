import numpy as np
import geopandas as gpd
from shapely.geometry import LineString, Point

# INPUT
# List of NP.ARRAYs with data

class LinestringSelector(object):

    def __init__(self, Istops, Fstops):
        self.data = gpd.read_file("./data/bus routes.geojson")
        self.SlicedLineStringList = []
        self.Istops = Istops
        self.Fstops = Fstops

    def _preprocess_data(self):
        """
        Creates tuples of type (bus_id, starting_point, ending_point)
        """

        start_final_points_array = []

        for _ , initial_stop in self.Istops.iterrows():
            initial_point = initial_stop['point']
            bus_id = initial_stop['bus_id']

            relevant_final_points = np.array(self.Fstops['bus_id'] == str(bus_id))
            final_stops = self.Fstops[relevant_final_points]

            for _ , final_stop in final_stops.iterrows():
                final_point = final_stop['point']
                points_tuple = (bus_id, initial_point, final_point)
                start_final_points_array.append(points_tuple)

        return start_final_points_array

    def get_sliced_routes(self):
        """
        Returns an array of type [ (bus_id, sliced_linestring), ... ]
        """

        sliced_linestrings_array = []

        # Get all tuples to analyse
        tuples_array = self._preprocess_data()

        # For each tuple:
        for bus_start_stop_tuple in tuples_array:
            # Pick all the dataframe rows of that bus line
            possible_linestrings = self.data['linea'] == bus_start_stop_tuple[0]
            selected_linestrings = self.data[possible_linestrings]

            # Foreach linestring:
            for linestring in selected_linestrings['geometry']:
                # Get the sliced LineString & append to array
                sliced_linestring = self._get_sliced_multi_linestring(linestring,
                                                                      bus_start_stop_tuple[1],
                                                                      bus_start_stop_tuple[2])

                sliced_linestrings_array.append(sliced_linestring)

        return sliced_linestrings_array


    def _convert_to_multilinestring(self, linestring):
        """
        Creates a collection of LineStrings that compose the original LineString
        """

        linestring_array = []

        # For num_of_points
        for i in range(len(linestring.coords) - 1):
            # Pick two consectuive points
            first_point = Point(linestring.coords[i])
            second_point = Point(linestring.coords[i + 1])
            # Create new LineString with those points
            linestring_new = LineString([first_point, second_point])
            linestring_array.append(linestring_new)

        return np.asarray(linestring_array, dtype=LineString)


    def _get_sliced_multi_linestring(self, linestring, starting_point, finishing_point):
        """
        Created and returns the sliced LineString
        """

        # Convert original LineString to MultiLineString
        multi_linestring = self._convert_to_multilinestring(linestring)
        # Get index of the nearest LineString to the starting stop
        starting_index = self._get_index_of_min_distance(multi_linestring, starting_point)
        # Get index of the nearest LineString to the final stop
        finishing_index = self._get_index_of_min_distance(multi_linestring, finishing_point)

        # TODO check index order to apply logic (if starting comes latter than finishing then do logic)
        # If the start_index is before the finishing_index (original LineString is ordered)
        if starting_index < finishing_index:
            # Get only the relevant LineStrings
            sliced_multi_linestring = multi_linestring[starting_index:finishing_index]
            return sliced_multi_linestring

        elif finishing_index < starting_index:
            # TODO check a scenario to see what could be done
            raise Exception("Not yet implemented")

        else:
            # TODO can they be equal? Should not be
            raise Exception("This case shouldn't be possible")

    def _convert_to_linestring(self, multi_linestring):
        """
        Creates LineString from multiple LineStrings
        """

        return LineString(multi_linestring)

    def _get_index_of_min_distance(self, multi_linestring, point):
        """
        Returns the index of the nearest LineString to a given point

        This method is used to get the index of the nearest LineString to a bus
        stop, which, depending if it's a final bus stop or the initial one, will be
        used to slice the multi_linestring arraty in order to get only the relevant
        portion of the original LineString
        """

        distances = []

        for linestring in multi_linestring:
            dist = linestring.distance(point)
            distances.append(dist)

        return distances.index(min(distances))