import json

import geopandas as gpd
import pathlib
from shapely.geometry import Point
import numpy as np

# Find the common bus lines among an Initial list of points and a Final list of points
# The Initial list should contain at least one Point
# The Final list should contain at least one Point
def _find_common_bus_lines(Ilist: list, Flist: list):
    # Checking the input format
    # Check the lengths of the input lists are greater than 0
    if len(Ilist) <= 0:
        raise Exception("Initial list should contain at least a point")
    elif len(Flist) <= 0:
        raise Exception("Final list should contain at least a point")
    else:
        starting_lines = [element[0] for element in Ilist]
        ending_lines = [element[0] for element in Flist]
        common_lines = [line for line in starting_lines if line in ending_lines]
        return common_lines


# Find the interception between two set of stops
# The Initial list should contain at least one Point
# The Final list should contain at least one Point
def intercept(Ilist: list, Flist: list):
    # Checking the input format
    # Check the lengths of the input lists are greater than 0
    if len(Ilist) <= 0:
        raise Exception("Initial list should contain at least a point")
    elif len(Flist) <= 0:
        raise Exception("Final list should contain at least a point")
    else:
        # Find the lines that are in both lists
        common_lines = _find_common_bus_lines(Ilist, Flist)
        # Find the common lines contained in the initial list
        filtered_IList = list(set([element for element in Ilist if element[0] in common_lines]))
        # Find the common lines contained in the final list
        filtered_FList = list(set([element for element in Flist if element[0] in common_lines]))
        # Wrap them in a geopanda dataframe
        result_IDataframe = gpd.GeoDataFrame(filtered_IList, columns=['bus_id', 'longitude', 'latitude'])
        result_IDataframe['point'] = [Point(float(e[1]), float(e[2])) for e in filtered_IList]
        result_FDataframe = gpd.GeoDataFrame(filtered_FList, columns=['bus_id', 'longitude', 'latitude'])
        result_FDataframe['point'] = [Point(float(e[1]), float(e[2])) for e in filtered_FList]
        return result_IDataframe, result_FDataframe

# Class that manages the stops
class stops(object):

    def __init__(self, type_of_dataset="BUS"):
        # Finding the path of the bus stops geoson
        current_dir = pathlib.Path(__file__).parent.parent
        if type_of_dataset is "BUS":
            routes_file = current_dir.joinpath("data/bus_data.geojson")
        elif type_of_dataset is "TRAIN":
            routes_file = current_dir.joinpath("data/train_data.geojson")
        else:
            raise Exception("type of dataset should be BUS or TRAIN, other datasets are not implemented yet.")
        f = open(routes_file)
        data = json.load(f)
        nodes = [feature for feature in data['features'] if 'node' in feature['id']]
        lines_and_stops = []
        # For each node creates a tuple and append it to buses and stops
        for node in nodes:
            longitude = float(node['geometry']['coordinates'][0])
            latitude = float(node['geometry']['coordinates'][1])
            for line in node['properties']['@relations']:
                if 'ref' in line['reltags']:
                    lines_and_stops.append((line['reltags']['ref'], longitude, latitude))
        lines_and_stops = np.array(lines_and_stops)
        # Creating the geopanda dataframe
        dataset = gpd.GeoDataFrame()
        dataset['linea'] = lines_and_stops[:, 0]
        dataset['longitude'] = lines_and_stops[:, 1]
        dataset['latitude'] = lines_and_stops[:, 2]
        self.dataset = dataset

    # Search the stops from between a square [x0, x1, y0, y1]
    # It raises exception if the input are not well formatted
    def _search_indexes(self, from_x=0, to_x=0, from_y=0, to_y=0):
        if from_x > to_x:
            raise Exception("From_x should be less than the to_x")
        elif from_y > to_y:
            raise Exception("From_y should be less than the to_y")
        else:
            # # Computing the result
            # # Start by computing a partial result
            # partial_result = [record for record in self.dataset.values if
            #                   from_x < record[1] < to_x and from_y < record[2] < to_y]
            # result = []
            # for record in partial_result:
            #     bus_lines = record[4].split(',')
            #     for bus_id in bus_lines:
            #         new_record = record.copy()
            #         new_record[4] = bus_id
            #         result.append(new_record)
            # Computing the result
            # Start by computing a partial result
            result = [record for record in self.dataset.values if
                              from_x < float(record[1]) < to_x and from_y < float(record[2]) < to_y]
            return result

    # Find the bus stops close to this point with exponential backoff policy
    # The exponential backoff is used in order to find a minimum amount of stops
    def find_stops_close_to(self, p: Point, radius=0.0003080999999998113, minimum_amount_of_stops = 5):
        # Initialize the result to an empty list
        result = []
        i = 0
        while len(result) < 3 and i < 5:
            # Compute the coordinates of the rectangle used to find the stops
            from_x = p.x - radius
            from_y = p.y - radius
            to_x = p.x + radius
            to_y = p.y + radius
            result = self._search_indexes(from_x, to_x, from_y, to_y)
            # Exponential backoff policy
            radius = radius * 1.5
            i += 1
        return result

if __name__ == '__main__':
    s = stops()