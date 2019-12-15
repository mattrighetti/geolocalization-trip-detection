from shapely.geometry import Point

def parseGeoJSON(data):
    trip_coordinates = []
    for p in data['snappedPoints']:
        trip_coordinates.append(Point(p["location"]["longitude"],
                                      p["location"]["latitude"]))
    return trip_coordinates
