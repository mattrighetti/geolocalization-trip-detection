import json
import numpy as np
from shapely.geometry import LineString
import geopandas as gpd

if __name__ == '__main__':



    # BUSES
    f = open('data/bus_data.geojson')
    data = json.load(f)
    relations = [feature for feature in data['features'] if 'relation' in feature['id']]
    buses = np.array([x['properties']['ref'] for x in relations if 'ref' in x['properties']])
    buses = np.sort(buses)

    buses_and_routes = np.array([(x['properties']['ref'], x['geometry']) for x in relations if 'ref' in x['properties']])

    # Casting multilinestring into linestring
    for i in range(len(buses_and_routes)):
        bus = buses_and_routes[i][0]
        route = buses_and_routes[i][1]
        if route['type'] == 'MultiLineString':
            unique_linestring = []
            for linestring in route['coordinates']:
                unique_linestring += linestring
            buses_and_routes[i][1]['type'] = 'LineString'
            buses_and_routes[i][1]['coordinates'] = unique_linestring

    # Casting a dictionary (composed by 'type' and 'coordinates') into a linestring
    buses_and_linestrings = np.array([(x[0], LineString(x[1]['coordinates'])) for x in buses_and_routes])

    data = gpd.GeoDataFrame()
    data['linea'] = buses_and_linestrings[:, 0]
    data['geometry'] = buses_and_linestrings[:, 1]
    data['type'] = 'BUS'




    # TRAINS
    f = open('data/train_data.geojson')
    data = json.load(f)
    relations = [feature for feature in data['features'] if 'relation' in feature['id']]
    buses = np.array([x['properties']['ref'] for x in relations if 'ref' in x['properties']])
    buses = np.sort(buses)

    buses_and_routes = np.array([(x['properties']['ref'], x['geometry']) for x in relations if 'ref' in x['properties']])

    # Casting multilinestring into linestring
    for i in range(len(buses_and_routes)):
        bus = buses_and_routes[i][0]
        route = buses_and_routes[i][1]
        if route['type'] == 'MultiLineString':
            unique_linestring = []
            for linestring in route['coordinates']:
                unique_linestring += linestring
            buses_and_routes[i][1]['type'] = 'LineString'
            buses_and_routes[i][1]['coordinates'] = unique_linestring

    # Casting a dictionary (composed by 'type' and 'coordinates') into a linestring
    buses_and_linestrings = np.array([(x[0], LineString(x[1]['coordinates'])) for x in buses_and_routes])

    data = gpd.GeoDataFrame()
    data['linea'] = buses_and_linestrings[:, 0]
    data['geometry'] = buses_and_linestrings[:, 1]
    data['type'] = 'TRAIN'