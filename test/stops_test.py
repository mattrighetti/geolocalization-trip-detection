import unittest

import geopandas
from shapely.geometry import Point

from Utils.stops import stops, intercept, _find_common_bus_lines


# Testing the dataset is correctly loaded in memory
def test_loading_dataset():
    print("Checking the type of the dataset.")
    print("It should be a geopandas.geodataframe.GeoDataFrame .")
    geo_dataframe = stops().dataset

    # Check that the initialized dataframe is not empty
    assert isinstance(geo_dataframe, geopandas.geodataframe.GeoDataFrame)
    print("Test passed.\n")


# Testing the bus stops to the Duomo
def test_find_bus_stops_close_to_Duomo():
    print("Checking the find bus stops close to Duomo, Milan")
    x = 9.18951
    y = 45.46427
    p = Point(x, y)
    radius = 0.0015
    closest_stops = stops().find_stops_close_to(p, radius)

    # Check that there are some stops close to the Duomo
    assert len(closest_stops) > 0
    print(f"The number of stops is greater than 0, they are {len(closest_stops)}")

    # Check that those buses are stopping near the Duomo
    bus_lines_to_check = ['12', '16', '19']
    print(f"Looking if the bus lines {bus_lines_to_check} are in the closest stops")
    bus_lines_in_the_closest_stops = set([stop[0] for stop in closest_stops])
    is_the_bus_line_contained = [bus_line in bus_lines_in_the_closest_stops for bus_line in bus_lines_to_check]
    print(f"Are they contained? {is_the_bus_line_contained}")
    assert all(is_the_bus_line_contained) is True
    print("Test passed.\n")


# Testing the bus stops to the Porta Genova
def test_find_bus_stops_close_to_Porta_Genova():
    print("Checking the find bus stops close to Porta Genova, Milan")
    x = 9.174606
    y = 45.456665
    p = Point(x, y)
    radius = 0.0015
    closest_stops = stops().find_stops_close_to(p, radius)

    # Check that there are some stops close to Porta Genova
    assert len(closest_stops) > 0
    print(f"The number of stops is greater than 0, they are {len(closest_stops)}")

    # Check that those buses are stopping near Porta Genova
    bus_lines_to_check = ['2', '14']
    print(f"Looking if the bus lines {bus_lines_to_check} are in the closest stops")
    bus_lines_in_the_closest_stops = set([stop[0] for stop in closest_stops])
    is_the_bus_line_contained = [bus_line in bus_lines_in_the_closest_stops for bus_line in bus_lines_to_check]
    print(f"Are they contained? {is_the_bus_line_contained}")
    assert all(is_the_bus_line_contained) is True
    print("Test passed.\n")


# Testing the bus stops to the politecnico
def test_find_bus_stops_close_to_Politecnico():
    print("Checking the find bus stops close to Politecnico, Milan")
    x = 9.226182
    y = 45.478657
    p = Point(x, y)
    radius = 0.0015
    closest_stops = stops().find_stops_close_to(p, radius)

    # Check that there are some stops close to Politecnico
    assert len(closest_stops) > 0
    print(f"The number of stops is greater than 0, they are {len(closest_stops)}")

    # Check that those buses are stopping near Politecnico
    bus_lines_to_check = ['19', '33']
    print(f"Looking if the bus lines {bus_lines_to_check} are in the closest stops")
    bus_lines_in_the_closest_stops = set([stop[0]
                                          for stop
                                          in closest_stops])
    is_the_bus_line_contained = [bus_line in bus_lines_in_the_closest_stops
                                 for bus_line
                                 in bus_lines_to_check]
    print(f"Are they contained? {is_the_bus_line_contained}")
    assert all(is_the_bus_line_contained) is True
    print("Test passed.\n")


# Testing that there is at least one bus line from Duomo to Polimi
def test_intercept_from_Duomo_to_Politecnico():
    print("Intercepting the 'from' dataset with the 'to' dataset")
    duomo_x = 9.18951
    duomo_y = 45.46427
    duomo_coordinate = Point(duomo_x, duomo_y)
    politecnico_x = 9.226182
    politecnico_y = 45.478657
    politecnico_coordinate = Point(politecnico_x, politecnico_y)
    radius = 0.0015
    duomo_stops = stops().find_stops_close_to(duomo_coordinate, radius)
    polimi_stops = stops().find_stops_close_to(politecnico_coordinate, radius)
    relevant_duomo_stops, relevant_politecnico_stops = intercept(duomo_stops, polimi_stops)

    # Check the format of the output
    assert isinstance(relevant_duomo_stops, geopandas.geodataframe.GeoDataFrame)
    assert isinstance(relevant_politecnico_stops, geopandas.geodataframe.GeoDataFrame)
    print("The returned datasets are both GeoDataframes, Great.")
    expected_columns = ['bus_id', 'longitude', 'latitude', 'point']
    does_result_contains_the_expected_columns = [column in relevant_duomo_stops.columns
                                                 for column
                                                 in expected_columns]
    assert all(does_result_contains_the_expected_columns) is True
    does_result_contains_the_expected_columns = [column in relevant_politecnico_stops.columns
                                                 for column
                                                 in expected_columns]
    assert all(does_result_contains_the_expected_columns) is True
    print(f"The result contains those columns {expected_columns}")

    # Check that only the bus line '19' is contained in both dataset
    duomo_lines = set(relevant_duomo_stops['bus_id'])
    politecnico_lines = set(relevant_politecnico_stops['bus_id'])
    assert len(duomo_lines) == 1
    assert len(politecnico_lines) == 1
    assert '19' in politecnico_lines
    assert '19' in duomo_lines
    print("Only line '19' connects Duomo to Politecnico")
    print("Test passed.\n")


# Testing exceptions
def test_intercept_exception():
    print("Testing interception error")
    try:
        intercept([], [])
        assert False
    except:
        assert True
        print("Test passed.\n")


def test_find_common_line_bus_exception():
    print("Testing find common bus lines error")
    try:
        _find_common_bus_lines([], [])
        assert False
    except:
        assert True
        print("Test passed.\n")


if __name__ == '__main__':
    test_loading_dataset()
    test_find_bus_stops_close_to_Duomo()
    test_find_bus_stops_close_to_Porta_Genova()
    test_find_bus_stops_close_to_Politecnico()
    test_intercept_from_Duomo_to_Politecnico()
    test_intercept_exception()
    test_find_common_line_bus_exception()
