import json

from flask import Flask
from flask import request
from shapely.geometry import Point

from Utils.DataParser import DataParser
from algorithm import elaborate_request
import os
import geopandas as gpd
from Utils.NetworkManager import send_data
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

    try:
        req = request.get_json()
        print(req)
        geojson = req['data']
        start_time = req['start_time']
        end_time = req['end_time']
        if not start_time:
            return 'start_time missing', 500
        if not end_time:
            return 'end_time missing', 500
        if not data:
            return 'Data missing', 500
    
        dataParser = DataParser()
        user_route_dict = dataParser.parse(geojson)
        raw_user_route = user_route_dict['raw']
        snapped_user_route = user_route_dict['snapped']
        result = elaborate_request(user_id=user_id, ticket_id=ticket_id, start_time=start_time, end_time=end_time, raw_data=raw_user_route, snapped_data=snapped_user_route)
    
        # if a match is found
        if result['transportation'] != None:
            # Send the result of the algorithm to the Java Backend
            send_data(result)
            app.logger.info("SUCCESS - km_travelled: %f \tvehicle: %s ", result['km_travelled'], result['transportation'])
            return result, 200
        else:
            return "Match not found", 200
    except Exception as message:
    #     # TODO Don't return 200 but another status code
        return "Something went wrong " + str(message), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001' , debug=True)
