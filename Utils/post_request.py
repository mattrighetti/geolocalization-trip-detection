import requests

def save_to_database(user_id, ticket_id, km_travelled):

    API_URL = "https://polimi-demo.partners.mia-platform.eu/v2/trips/"

    # TODO fix start_time & end_time
    data = {
        'user_id' : user_id,
        'ticket_id' : ticket_id,
        'km_travelled' : km_travelled,
        'transportation' : 'bus',
        'start_time' : 1,
        'end_time' : 3
    }

    r = requests.post(API_URL, data=data)

    if r.text == "200":
        return
    else:
        raise Exception("Couldn't contact the server...")