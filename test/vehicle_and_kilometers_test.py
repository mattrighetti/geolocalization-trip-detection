import geopandas as gpd
from algorithm import detect_vehicle_and_km

def test_90_route():
    response_points = "./data/test/response-points.geojson"
    rpdf = gpd.read_file(response_points)
    user_route = rpdf['geometry']

    vehicle, km_travelled = detect_vehicle_and_km(user_route)

    assert vehicle == "bus"
    print(km_travelled)
    
