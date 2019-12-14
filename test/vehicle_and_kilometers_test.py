import geopandas as gpd
from algorithm import detect_vehicle_and_km

def test_90_route():
    response_points = "./data/test/response-points.geojson"
    rpdf = gpd.read_file(response_points)
    user_route = rpdf['geometry']
    km_travelled = 0
    vehicle, km_travelled = detect_vehicle_and_km(user_route)
    uncertainty = 0.05

    print(km_travelled)
    assert vehicle == "bus"
    assert is_in_range(km_travelled, uncertainty) is True


def is_in_range(km_travelled:float, uncertainty: float):
    upper_bound = km_travelled + (km_travelled * uncertainty)
    lower_bound =  km_travelled - (km_travelled * uncertainty)
    return ((km_travelled >= lower_bound) and (km_travelled <= upper_bound))

    
