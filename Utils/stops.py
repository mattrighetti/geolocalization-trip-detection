import geopandas as gpd
import pathlib
from shapely.geometry import Point


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
        starting_lines = [element[4] for element in Ilist]
        ending_lines = [element[4] for element in Flist]
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
        filtered_IList = [element for element in Ilist if element[4] in common_lines]
        # Find the common lines contained in the final list
        filtered_FList = [element for element in Flist if element[4] in common_lines]
        # Wrap them in a geopanda dataframe
        result_IDataframe = gpd.GeoDataFrame(filtered_IList, columns=['id', 'x', 'y', 'location', 'bus_id', 'point'])
        result_FDataframe = gpd.GeoDataFrame(filtered_FList, columns=['id', 'x', 'y', 'location', 'bus_id', 'point'])
        return result_IDataframe, result_FDataframe

# Class that manages the stops
class stops(object):

    # Constructor
    # Loads the stops data structure in memory
    # Cleanse the input data
    def __init__(self):
        # Finding the path of the bus stops geoson
        current_dir = pathlib.Path(__file__).parent.parent
        routes_file = current_dir.joinpath("data/bus_stops.geojson")
        # Load the file in memory
        dfs = gpd.read_file(routes_file)
        points = dfs.geometry
        # Data cleaning and engineering
        x_coo = [point.x for point in points]
        y_coo = [point.y for point in points]
        dfs.insert(1, "y_coo", y_coo, True)
        dfs.insert(1, "x_coo", x_coo, True)
        dfs.sort_values(by=['x_coo', 'y_coo'], ascending=True, inplace=True)
        self.dataset = dfs

    # Search the stops from between a square [x0, x1, y0, y1]
    # It raises exception if the input are not well formatted
    def _search_indexes(self, from_x=0, to_x=0, from_y=0, to_y=0):
        if from_x > to_x:
            raise Exception("From_x should be less than the to_x")
        elif from_y > to_y:
            raise Exception("From_y should be less than the to_y")
        else:
            # Computing the result
            # Start by computing a partial result
            partial_result = [record for record in self.dataset.values if
                              from_x < record[1] < to_x and from_y < record[2] < to_y]
            result = []
            for record in partial_result:
                bus_lines = record[4].split(',')
                for bus_id in bus_lines:
                    new_record = record.copy()
                    new_record[4] = bus_id
                    result.append(new_record)
            return result

    # Find the bus stops close to this point with exponential backoff policy
    # The exponential backoff is used in order to find a minimum amount of stops
    def find_bus_stops_close_to(self, p: Point, radius=0.0003080999999998113, minimum_amount_of_stops = 5):
        # Initialize the result to an empty list
        result = []
        while len(result) < 3:
            # Compute the coordinates of the rectangle used to find the stops
            from_x = p.x - radius
            from_y = p.y - radius
            to_x = p.x + radius
            to_y = p.y + radius
            result = self._search_indexes(from_x, to_x, from_y, to_y)
            # Exponential backoff policy
            radius = radius * 1.5
        return result
