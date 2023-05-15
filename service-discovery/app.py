from datetime import datetime
from flask import Flask, request, jsonify
from config import system_config


app = Flask(__name__)
SERVICE_MAPPER = {}


def validate_request(data):
    return all([key in ['service-name', 'service-url', 'service-port', 'service-endpoints'] for key in data.keys()])


@app.route('/register', methods=['POST'])
def register():        
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Recieved request for service registration, beginning the validation.')
    if validate_request(dict(request.form)):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Service registration.')
        SERVICE_MAPPER[request.form['service-name']] = {
            'service-url': request.form['service-url'],
            'service-port': request.form['service-port'],
            'service-endpoints': request.form['service-endpoints']
            }
        return {'message': 'Service registered successfully.'}, 200

    print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] The recieved request did not pass the validation, cause it does not contain the neccessary keys.')
    return {'message': f'Bad request, cannot register the service, because it contains unknown keys {dict(request.form).keys()}.'}, 401


@app.route('/get-services', methods=['POST'])
def get_services():
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Recieved request to get the registered service information.')
    return SERVICE_MAPPER, 200


if __name__ == "__main__":
    app.run('0.0.0.0', port=system_config.SERVICE_DISCOVERY_PORT)