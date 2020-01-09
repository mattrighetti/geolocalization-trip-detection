import geopandas as gpd
from algorithm import detect_vehicle_and_km
from shapely.geometry import Point

response_points = './data/test/S6_UnitTest.geojson'
rpdf = gpd.read_file(response_points)
raw_data = rpdf['geometry']
real_km = 0.8
snapped_data = [Point(9.207112, 45.476559), Point(9.210908, 45.480275)]
vehicle, km_travelled = detect_vehicle_and_km(raw_user_route=raw_data, snapped_user_route=snapped_data)