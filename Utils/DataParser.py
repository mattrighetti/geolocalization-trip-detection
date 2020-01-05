from shapely.geometry import Point

class DataParser:
    
    def parse(self, data):
        dict_routes = {}
        dict_routes['snapped'] = self._parseGeoJSON(data, 'snappedPoints')
        dict_routes['raw'] = self._parseGeoJSON(data, 'rawData')

        return dict_routes

    def _parseGeoJSON(self, data, kind):
        trip_coordinates = []

        for p in data[kind]:
            longitude = p["location"]["longitude"]
            latitude = p["location"]["latitude"]
            point = self._create_point(longitude, latitude)
            trip_coordinates.append(point)

        return trip_coordinates

    def _create_point(self, longitude, latitude):
        return Point(longitude, latitude)