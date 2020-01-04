from Utils.routes_analyzer import routes_analyzer
import geopandas as gpd
import numpy as np
import pytest
from shapely.geometry import Point


def test_1():
    bus_routes = []
    route = create_bus_route()
    bus_routes.append(route)

    user_route = create_user_route()

    analyzer = routes_analyzer(bus_routes, user_route)

    metrics = analyzer.compute_metrics()

    assert len(metrics) > 0
    assert metrics[0]['number_user_coordinates'] == 3

#Test that an Exception is raised when the bus_routes list is empty
def test_bus_routes_emptiness():
    bus_routes = []

    #Assumption, user_route is not null (checked in the previous steps of the algorithm)
    user_route = create_user_route()

    analyzer = routes_analyzer(bus_routes, user_route)

    with pytest.raises(Exception):
        assert analyzer.compute_metrics()

#Test that an Exception is raised when the list in bus_routes does not contain Point
def test_bus_route_list_mismatch():
    p1 = Point(9.222919, 45.480466)
    bus_routes = np.array(p1)

    #Assumption, user_route is not null (checked in the previous steps of the algorithm)
    user_route = create_user_route()

    analyzer = routes_analyzer(bus_routes, user_route)

    with pytest.raises(Exception):
        assert analyzer.compute_metrics()

def test_bus_route_type_mismatch():
    bus_routes = [1,2,4]

    #Assumption, user_route is not null (checked in the previous steps of the algorithm)
    user_route = create_user_route()

    analyzer = routes_analyzer(bus_routes, user_route)

    with pytest.raises(Exception):
        assert analyzer.compute_metrics()

def create_user_route():
    user_route = []
    p1 = Point(9.222919, 45.480466)
    p2 = Point(9.223688, 45.478545)
    p3 = Point(9.222219, 45.478591)
    p4 = Point(9.224815, 45.477557)
    p5 = Point(9.230252, 45.477362)

    user_route.append(p1)
    user_route.append(p2)
    user_route.append(p3)
    user_route.append(p4)
    user_route.append(p5)

    return user_route

def create_bus_route():
    dataframe =  gpd.read_file('./data/test/90_track.geojson')
    bus_route = []

    for coordinate in dataframe['geometry'].iloc[0].coords:
        p = Point(coordinate)
        bus_route.append(p)
    
    return (bus_route, 'BUS')
