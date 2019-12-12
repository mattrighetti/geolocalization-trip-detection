import geopandas as gpd
from shapely.geometry import Point


def _find_common_bus_lines(Ilist: list, Flist: list):
    starting_lines = [element[4] for element in Ilist]
    ending_lines = [element[4] for element in Flist]
    common_lines = [line for line in starting_lines if line in ending_lines]
    return common_lines

def intercept(Ilist: list, Flist: list):
    common_lines = _find_common_bus_lines(Ilist, Flist)
    filtered_IList = [element for element in Ilist if element[4] in common_lines]
    filtered_FList = [element for element in Flist if element[4] in common_lines]
    result_IDataframe = gpd.GeoDataFrame(filtered_IList, columns=['id', 'x', 'y', 'location', 'bus_id', 'point'])
    result_FDataframe = gpd.GeoDataFrame(filtered_FList, columns=['id', 'x', 'y', 'location', 'bus_id', 'point'])
    return result_IDataframe, result_FDataframe

class stops(object):

    def __init__(self):
        stops = "./data/bus stops.geojson"
        dfs = gpd.read_file(stops)
        points = dfs.geometry
        x_coo = [point.x for point in points]
        y_coo = [point.y for point in points]
        dfs.insert(1, "y_coo", y_coo, True)
        dfs.insert(1, "x_coo", x_coo, True)
        dfs.sort_values(by=['x_coo', 'y_coo'], ascending=True, inplace=True)
        self.dataset = dfs

    def _search_indexes(self, from_x=0, to_x=0, from_y=0, to_y=0):
        assert from_x < to_x, "x coordinates range is wrong. from_x must be smaller than to_x"
        # TODO: use binary search
        partial_result = [record for record in self.dataset.values if from_x < record[1] < to_x and from_y < record[2] < to_y]
        result = []
        for record in partial_result:
            bus_lines = record[4].split(',')
            for bus_id in bus_lines:
                new_record = record.copy()
                new_record[4] = bus_id
                result.append(new_record)
        return result

    def find_bus_stops_close_to(self, p: Point, radius=0.001):
        from_x = p.x - radius
        from_y = p.y - radius
        to_x = p.x + radius
        to_y = p.y + radius
        return self._search_indexes(from_x, to_x, from_y, to_y)
