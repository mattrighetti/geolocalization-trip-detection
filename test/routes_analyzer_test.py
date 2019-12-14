from Utils.routes_analyzer import routes_analyzer
import geopandas as gpd
from shapely.geometry import Point


def test_1():
    routes_list = []
    route = create_route()
    routes_list.append(route)

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

    analyzer = routes_analyzer(routes_list, user_route)

    metrics = analyzer.compute_metrics()

    assert len(metrics) > 0
    print(metrics[0]["percentage_user"])
    print(metrics[0]["number_user_coordinates"])
    print(metrics[0]["percentage_poly"])
    print(metrics[0]["number_polygons"])
    assert metrics[0]["number_user_coordinates"] == 3


def create_route():
    dataframe =  gpd.read_file('./data/test/90_track.geojson')
    bus_route = []

    for coordinate in dataframe['geometry'].iloc[0].coords:
        p = Point(coordinate)
        bus_route.append(p)
    
    return bus_route
