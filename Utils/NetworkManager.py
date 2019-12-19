import requests
import json

def send_data(data):

    API_URL = "https://polimi-demo.partners.mia-platform.eu/geolocalization/trip"

    data = json.dumps(data)

    session = requests.Session()
    session.headers.update({'Content-Type' : 'application/json'})
    request = session.post(API_URL, data=data)
    session.close()
    if request.status_code == 200:
        return
    else:
        raise Exception("Couldn't contact the server... response message: " + str(request.text))