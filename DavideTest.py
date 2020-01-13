from shapely.geometry import LineString, Point
import geopandas as gpd
import pandas as pd
import numpy as np
import pathlib
import os
import json
import time
from geopy import distance

def _load_bus_data():

    bus_data_path = pathlib.Path(__file__).parent.joinpath("data/bus_processed_data.csv")
    try:
        print("Loading from cached file...")
        csv_file = pd.read_csv(bus_data_path)
        data = gpd.GeoDataFrame(csv_file)
        # Deserializing Linestring (as strings) to Linestring (as object)
        geometries = []
        for i in range(len(data['geometry'])):
            linestring_as_string = str(data['geometry'][i][12:-1])
            coordinates_as_string = linestring_as_string.split(", ")
            coordinates_as_pair = [coordinate_as_string.split(" ") for coordinate_as_string in coordinates_as_string]
            coordinates_as_float = [(float(coordinate[0]), float(coordinate[1])) for coordinate in coordinates_as_pair]
            linestring = LineString(coordinates_as_float)
            geometries.append(linestring)
        data['geometry'] = geometries
        print("Loading from cached file SUCCESS")
    except:
        print("Loading from cached file FAILED")
        # Read bus routes
        threshold_min_points = 50
        threshold_min_distance = 1
        current_dir = pathlib.Path(__file__).parent.parent
        routes_path = current_dir.joinpath("data/bus_data.geojson")
        bus_file = open(routes_path)
        data = json.load(bus_file)
        relations = [feature for feature in data['features'] if 'relation' in feature['id']]
        buses_and_routes = np.array(
            [(x['properties']['ref'], x['geometry']) for x in relations if 'ref' in x['properties']], dtype=object)
        buses_and_linestrings = self._convert_to_linestring(buses_and_routes, threshold_min_points,threshold_min_distance)
        data = gpd.GeoDataFrame()
        data['linea'] = buses_and_linestrings[:, 0]
        data['geometry'] = buses_and_linestrings[:, 1]
        data['type'] = 'BUS'
        data.to_csv('./data/bus_processed_data.csv')
    return data

def _load_train_data():
    train_data_path = pathlib.Path(__file__).parent.joinpath("data/train_processed_data.csv")
    try:
        print("Loading from cached file...")
        csv_file = pd.read_csv(train_data_path)
        data = gpd.GeoDataFrame(csv_file)
        # Deserializing Linestring (as strings) to Linestring (as object)
        geometries = []
        for i in range(len(data['geometry'])):
            linestring_as_string = str(data['geometry'][i][12:-1])
            coordinates_as_string = linestring_as_string.split(", ")
            coordinates_as_pair = [coordinate_as_string.split(" ") for coordinate_as_string in coordinates_as_string]
            coordinates_as_float = [(float(coordinate[0]), float(coordinate[1])) for coordinate in coordinates_as_pair]
            linestring = LineString(coordinates_as_float)
            geometries.append(linestring)
        data['geometry'] = geometries
        print("Loading from cached file SUCCESS")
    except:
        print("Loading from cached file FAILED")
        # Read train routes
        threshold_min_points = 35
        threshold_min_distance = 1
        current_dir = pathlib.Path(__file__).parent.parent
        routes_path = current_dir.joinpath("data/train_data.geojson")
        train_file = open(routes_path)
        data = json.load(train_file)
        relations = [feature for feature in data['features'] if 'relation' in feature['id']]
        trains_and_routes = np.array(
            [(x['properties']['ref'], x['geometry']) for x in relations if 'ref' in x['properties']], dtype=object)
        trains_and_linestrings = self._convert_to_linestring(trains_and_routes, threshold_min_points, threshold_min_distance)
        data = gpd.GeoDataFrame()
        data['linea'] = trains_and_linestrings[:, 0]
        data['geometry'] = trains_and_linestrings[:, 1]
        data['type'] = 'TRAIN'
        data.to_csv('./data/train_processed_data.csv')
    return data



if __name__ == '__main__':

    bus = _load_bus_data()
    train = _load_train_data()

