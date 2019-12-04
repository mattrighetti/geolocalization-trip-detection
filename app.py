from flask import Flask
from flask import request

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

@app.route('/datatrip', methods=['POST'])
def datatrip():
    assert request.path == '/datatrip'
    assert request.method == 'POST'

    req = request.get_json()
    user_id = req['user_id']
    ticket_id = req['ticket_id']
    data = req['data']
    if (not user_id):
        return ('User_id missing', 500)
    if (not ticket_id):
        return ('Ticket_id missing', 500)
    if (not data):
        return ('Data missing', 500)
    return 'Data retrieved'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
