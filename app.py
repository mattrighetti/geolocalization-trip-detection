import json

from flask import Flask
from flask import request
from Utils.parseGeoJSON import parseGeoJSON
from algorithm import elaborate_request
import os
import geopandas as gpd
from algorithm import detect_vehicle_and_km

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/-/ready')
def ready():
    return 'ready'


@app.route('/-/healtz')
def healtz():
    return 'healtz'


@app.route('/<int:user_id>/<int:ticket_id>/data', methods=['POST'])
def data(user_id, ticket_id):
    assert request.method == 'POST'

    req = request.get_json()
    geojson = req['data']
    start_time = req['start_time']
    end_time = req['end_time']
    if not start_time:
        return 'start_time missing', 500
    if not end_time:
        return 'end_time missing', 500
    if not data:
        return 'Data missing', 500
    print(geojson)
    print()
    random_filename = "wow.geojson"
    file = open(random_filename, "w+")
    file.write(str(geojson).replace("'", "\""))
    file.close()
    geodataframe = gpd.read_file(random_filename)

    print(geodataframe.head())
    x = elaborate_request(user_id=user_id, ticket_id=ticket_id, start_time=start_time, end_time=end_time,
                          data=geodataframe['geometry'])
    print(x)
    return 'Data retrieved'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
