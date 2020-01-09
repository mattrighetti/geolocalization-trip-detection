import geopandas as gpd
from algorithm import detect_vehicle_and_km
from shapely.geometry import Point

#def test_90_route():
#    response_points = './data/test/response-points.geojson'
#    rpdf = gpd.read_file(response_points)
#    snapped_data = rpdf['geometry']
#    real_km = 0.8
#    raw_data = [Point(9.224007, 45.4595246), Point(9.1906667, 45.320449)]
#    vehicle, km_travelled = detect_vehicle_and_km(raw_user_route=raw_data, snapped_user_route=snapped_data)
#    uncertainty = 0.05
#
#    print('km')
#    print(km_travelled)
#    print('---------')
#    assert vehicle == 'BUS'
#    assert is_in_range(km_travelled, uncertainty, real_km) is True

def test_S6_route():
    response_points = './data/test/S6_UnitTest.geojson'
    rpdf = gpd.read_file(response_points)
    raw_data = rpdf['geometry']
    real_km = 0.8
    snapped_data = [Point(9.207112, 45.476559), Point(9.210908, 45.480275)]
    vehicle, km_travelled = detect_vehicle_and_km(raw_user_route=raw_data, snapped_user_route=snapped_data)
    uncertainty = 0.05

    print('km')
    print(km_travelled)
    print('---------')
    assert vehicle == 'BUS'
    assert is_in_range(km_travelled, uncertainty, real_km) is True


def is_in_range(km_travelled:float, uncertainty: float, real_km: float):
    upper_bound = real_km + (real_km * uncertainty)
    lower_bound =  real_km - (real_km * uncertainty)
    return ((km_travelled >= lower_bound) and (km_travelled <= upper_bound))

    
