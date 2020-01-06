from shapely.geometry import LineString, Point
import geopandas as gpd
import numpy as np
import pathlib
import os
import json
from geopy import distance


# INPUT
# List of NP.ARRAYs with data

class LinestringSelector(object):

    def __init__(self, Istops, Fstops, type_of_dataset="BUS"):

        # Check if data is correct
        self.check_data(Istops, Fstops)

        if type_of_dataset is "BUS":
            self.data = self._load_bus_data()
        elif type_of_dataset is "TRAIN":
            self.data = self._load_train_data()
        else:
            raise Exception("type of dataset should be BUS or TRAIN, other datasets are not implemented yet.")
        self.SlicedLineStringList = []
        self.Istops = Istops
        self.Fstops = Fstops

    def _load_bus_data(self):
        # Read bus routes
        threshold_min_points = 50
        threshold_min_distance = 1

        current_dir = pathlib.Path(__file__).parent.parent
        routes_path = current_dir.joinpath("data/bus_data.geojson")
        bus_file = open(routes_path)
        data = json.load(bus_file)
        relations = [feature for feature in data['features'] if 'relation' in feature['id']]

        buses_and_routes = np.array(
            [(x['properties']['ref'], x['geometry']) for x in relations if 'ref' in x['properties']], dtype=object)

        temp_buses_and_routes = []
        # Casting multilinestring into linestring
        for i in range(len(buses_and_routes)):
            bus = buses_and_routes[i][0]
            route = buses_and_routes[i][1]
            if route['type'] == 'MultiLineString':

                print(f"bus is {bus}")
                r = []

                # Step 1, retrieve the size of the linestrings
                size_of_the_linestrings = np.array([len(line) for line in route['coordinates']])
                print(size_of_the_linestrings)

                # Step 2, delete the linestrings that have a size less than the threshold 'threshold_min_points'
                filter_mask = size_of_the_linestrings > threshold_min_points
                print(filter_mask)
                filtered_linestrings = np.array([line for line in route['coordinates']])[filter_mask]

                # Step 2.1, if all linestrings are deleted, do not add the bus to the dataset
                if len(filtered_linestrings) == 0:
                    print(f'bus line {bus} has been discarded')
                    continue

                # Step 3, add the longest linestring to the route
                size_of_the_filtered_linestrings = np.array([len(line) for line in filtered_linestrings])
                max_size = max(size_of_the_filtered_linestrings)
                filter_max_mask = size_of_the_filtered_linestrings == max_size
                longest_linestring = filtered_linestrings[filter_max_mask][0]

                # Removing the linestring from the ones which can choose
                filtered_linestrings = list(filtered_linestrings)
                filtered_linestrings.remove(longest_linestring)

                r += longest_linestring
                initial_point_of_r = r[0]
                final_point_of_r = r[-1]

                # Exit condition
                while len(filtered_linestrings) != 0:
                    distance_matrix = []
                    # Step 4, compute the distance (head-tail, tail-head) from each linestring to the route
                    for line in filtered_linestrings:
                        # Compute distance from r-head
                        p1 = line[-1]
                        p2 = initial_point_of_r
                        p1 = (p1[1], p1[0])
                        p2 = (p2[1], p2[0])
                        distance_from_head = distance.geodesic(p1, p2, ellipsoid='Intl 1924').km

                        # Compute distance from r-tail
                        p1 = line[0]
                        p2 = final_point_of_r
                        p1 = (p1[1], p1[0])
                        p2 = (p2[1], p2[0])
                        distance_from_tail = distance.geodesic(p1, p2, ellipsoid='Intl 1924').km

                        distance_matrix += [(line, distance_from_head, distance_from_tail)]

                    # Step 5, select the closest linestring to the route (if the distance is less than 'threshold_min_distance'

                    # Searching for the line with min distance
                    min_distance_line = None
                    is_it_from_head = True
                    min_distance = float('inf')
                    for element in distance_matrix:
                        line = element[0]
                        distance_from_head = element[1]
                        distance_from_tail = element[2]
                        if min_distance > distance_from_head:
                            min_distance = distance_from_head
                            min_distance_line = line
                            is_it_from_head = True
                        if min_distance > distance_from_tail:
                            min_distance = distance_from_tail
                            min_distance_line = line
                            is_it_from_head = False

                    if min_distance < threshold_min_distance:
                        print(f"\tbefore {len(r)}")
                        if is_it_from_head:
                            temp = min_distance_line + r
                            r = temp
                        else:
                            temp = r + min_distance_line
                            r = temp
                        print(f"\tafter {len(r)}")
                        filtered_linestrings.remove(min_distance_line)
                    else:
                        break
                temp_buses_and_routes.append([bus, {'type': 'LineString', 'coordinates': r}])
                # buses_and_routes[i][1]['type'] = 'LineString'
                # buses_and_routes[i][1]['coordinates'] = r

        buses_and_routes = temp_buses_and_routes
        # Casting a dictionary (composed by 'type' and 'coordinates') into a linestring
        buses_and_linestrings = np.array([(x[0], LineString(x[1]['coordinates'])) for x in buses_and_routes],
                                         dtype=object)

        data = gpd.GeoDataFrame()
        data['linea'] = buses_and_linestrings[:, 0]
        data['geometry'] = buses_and_linestrings[:, 1]
        data['type'] = 'BUS'
        return data

    def _load_train_data(self):
        # Read train routes
        threshold_min_points = 35
        threshold_min_distance = 1

        current_dir = pathlib.Path(__file__).parent.parent
        routes_path = current_dir.joinpath("data/train_data.geojson")
        train_file = open(routes_path)
        data = json.load(train_file)
        relations = [feature for feature in data['features'] if 'relation' in feature['id']]

        trains_and_routes = np.array(
            [(x['properties']['name'], x['geometry']) for x in relations], dtype=object)

        temp_trains_and_routes = []
        # Casting multilinestring into linestring
        for i in range(len(trains_and_routes)):
            train = trains_and_routes[i][0]
            route = trains_and_routes[i][1]
            if route['type'] == 'MultiLineString':

                print(f"train is {train}")
                r = []

                # Step 1, retrieve the size of the linestrings
                size_of_the_linestrings = np.array([len(line) for line in route['coordinates']])
                print(size_of_the_linestrings)

                # Step 2, delete the linestrings that have a size less than the threshold 'threshold_min_points'
                filter_mask = size_of_the_linestrings > threshold_min_points
                print(filter_mask)
                filtered_linestrings = np.array([line for line in route['coordinates']])[filter_mask]

                # Step 2.1, if all linestrings are deleted, do not add the train to the dataset
                if len(filtered_linestrings) == 0:
                    print(f'train line {train} has been discarded')
                    continue

                # Step 3, add the longest linestring to the route
                size_of_the_filtered_linestrings = np.array([len(line) for line in filtered_linestrings])
                max_size = max(size_of_the_filtered_linestrings)
                filter_max_mask = size_of_the_filtered_linestrings == max_size
                longest_linestring = filtered_linestrings[filter_max_mask][0]

                # Removing the linestring from the ones which can choose
                filtered_linestrings = list(filtered_linestrings)
                filtered_linestrings.remove(longest_linestring)

                r += longest_linestring
                initial_point_of_r = r[0]
                final_point_of_r = r[-1]

                # Exit condition
                while len(filtered_linestrings) != 0:
                    distance_matrix = []
                    # Step 4, compute the distance (head-tail, tail-head) from each linestring to the route
                    for line in filtered_linestrings:
                        # Compute distance from r-head
                        p1 = line[-1]
                        p2 = initial_point_of_r
                        p1 = (p1[1], p1[0])
                        p2 = (p2[1], p2[0])
                        distance_from_head = distance.geodesic(p1, p2, ellipsoid='Intl 1924').km

                        # Compute distance from r-tail
                        p1 = line[0]
                        p2 = final_point_of_r
                        p1 = (p1[1], p1[0])
                        p2 = (p2[1], p2[0])
                        distance_from_tail = distance.geodesic(p1, p2, ellipsoid='Intl 1924').km

                        distance_matrix += [(line, distance_from_head, distance_from_tail)]

                    # Step 5, select the closest linestring to the route (if the distance is less than 'threshold_min_distance')

                    # Searching for the line with min distance
                    min_distance_line = None
                    is_it_from_head = True
                    min_distance = float('inf')
                    for element in distance_matrix:
                        line = element[0]
                        distance_from_head = element[1]
                        distance_from_tail = element[2]
                        if min_distance > distance_from_head:
                            min_distance = distance_from_head
                            min_distance_line = line
                            is_it_from_head = True
                        if min_distance > distance_from_tail:
                            min_distance = distance_from_tail
                            min_distance_line = line
                            is_it_from_head = False

                    if min_distance < threshold_min_distance:
                        print(f"\tbefore {len(r)}")
                        if is_it_from_head:
                            temp = min_distance_line + r
                            r = temp
                        else:
                            temp = r + min_distance_line
                            r = temp
                        print(f"\tafter {len(r)}")
                        filtered_linestrings.remove(min_distance_line)
                    else:
                        break
                temp_trains_and_routes.append([train, {'type': 'LineString', 'coordinates': r}])
                # trains_and_routes[i][1]['type'] = 'LineString'
                # trains_and_routes[i][1]['coordinates'] = r

        trains_and_routes = temp_trains_and_routes
        # Casting a dictionary (composed by 'type' and 'coordinates') into a linestring
        trains_and_linestrings = np.array([(x[0], LineString(x[1]['coordinates'])) for x in trains_and_routes],
                                         dtype=object)

        data = gpd.GeoDataFrame()
        data['linea'] = trains_and_linestrings[:, 0]
        data['geometry'] = trains_and_linestrings[:, 1]
        data['type'] = 'TRAIN'
        return data

    def check_data(self, Istops, Fstops):
        """
        Checks if data is correct

        @param Istops: list of Point
        @param Fstops: list of Point
        @return: None
        """

        # If not iterable it will throw an Exception saying that Istops or Fstops doesn't have len()
        Istops_len = len(Istops)
        Fstops_len = len(Fstops)

        # If Istops or Fstops is empty, throw an exception
        if Istops_len == 0 | Fstops_len == 0:
            raise Exception("Istops is empty.")

    def _preprocess_data(self):
        """
        Creates list tuples of type (bus_id, starting_point, ending_point)

        @return: list of tuples
        """

        start_final_points_array = []

        for _, initial_stop in self.Istops.iterrows():
            initial_point = initial_stop['point']
            bus_id = initial_stop['bus_id']

            relevant_final_points = np.array(self.Fstops['bus_id'] == str(bus_id))
            final_stops = self.Fstops[relevant_final_points]

            for _, final_stop in final_stops.iterrows():
                final_point = final_stop['point']
                points_tuple = (bus_id, initial_point, final_point)
                start_final_points_array.append(points_tuple)

        return start_final_points_array

    def to_list_of_points(self, linestrings_array):
        """
        Converts bus route LineString to a list of Points

        @param linestrings_array: LineString object
        @return: list of Points
        """
        bus_lines = []
        route_points = []

        for bus_line in linestrings_array:
            for linestring in bus_line:
                p1 = Point(linestring.coords[0])
                assert type(p1) == Point
                p2 = Point(linestring.coords[1])
                route_points.append(p1)
                route_points.append(p2)
            route_points = self._remove_duplicates(route_points)
            bus_lines.append(route_points)

        return bus_lines

    def get_sliced_routes(self):
        """
        Creates and returns a list of sliced_linestring with its associate bus_id

        sliced_linestring is a linestring constructed from the original bus routed removing the part not travelled by the user

        @return: array of type [ (bus_id, sliced_linestring), ... ]
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
                if sliced_linestring is not None:
                    sliced_linestrings_array.append(sliced_linestring)

        route_points = self.to_list_of_points(sliced_linestrings_array)
        return route_points

    def _convert_to_multilinestring(self, linestring):
        """
        Creates a collection of LineStrings that compose the original LineString and returns it.

        @param linestring: LineString object
        @return: collection of LineString that linestring is composed of
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
        Created and returns the sliced Multi-LineString

        @param linestring: LineString object
        @param starting_point: Point object that indicates where the user started his/her trip
        @param finishing_point: Point object that indicates where the user finished his/her trip
        @return: returns the original multi_linestring without the LineStrings not travelled by the user
        """

        # Convert original LineString to MultiLineString
        multi_linestring = self._convert_to_multilinestring(linestring)
        # Get index of the nearest LineString to the starting stop
        starting_index = self._get_index_of_min_distance(multi_linestring, starting_point)
        # Get index of the nearest LineString to the final stop
        finishing_index = self._get_index_of_min_distance(multi_linestring, finishing_point)

        # TODO check index order to apply logic (if starting comes latter than finishing then do logic)
        # If the start_index is before the finishing_index (original LineString is ordered)
        if starting_index <= finishing_index:
            # Get only the relevant LineStrings
            sliced_multi_linestring = multi_linestring[starting_index:finishing_index]
            return sliced_multi_linestring

        elif finishing_index < starting_index:
            # TODO check a scenario to see what could be done
            # raise Exception("Not yet implemented")
            return None
        else:
            # TODO can they be equal? Should not be
            # raise Exception("This case shouldn't be possible")
            return None

    def _convert_to_linestring(self, multi_linestring):
        """
        Creates LineString from multiple LineStrings

        @param multi_linestring: Collection of LineString object
        @return: LineString object created by joining a collection of multi_linestring into a single one
        """

        return LineString(multi_linestring)

    def _get_index_of_min_distance(self, multi_linestring, point):
        """
        Returns the index of the nearest LineString to a given point

        This method is used to get the index of the nearest LineString to a bus
        stop, which, depending if it's a final bus stop or the initial one, will be
        used to slice the multi_linestring arraty in order to get only the relevant
        portion of the original LineString

        @param multi_linestring: Collection of LineString object
        @param point: Point object
        @return: nearest LineString index in a LineString collection to point
        """

        distances = []

        for linestring in multi_linestring:
            dist = linestring.distance(point)
            distances.append(dist)

        return distances.index(min(distances))

    def _remove_duplicates(self, points: list):
        """
        Removed duplicate points in a list

        @param points: list of Points objects
        @return: List of unique Point objects
        """
        unique_list = []

        for point in points:
            if point not in unique_list:
                unique_list.append(point)

        return unique_list
