import json
import warnings
import requests
from datetime import datetime

from flask import Flask, request
from config import system_config
from scheduler import gna_scheduler, generate_population, select_best_schedule


warnings.filterwarnings("ignore")


app = Flask(__name__)


class AccessToken:
    def __init__(self) -> None:
        self.access_token = None
        self.token_lifespan = None
        self.generated_timestamp = None

    def estimate_lifespan(self, generated_timestamp, current_timestamp):
        if generated_timestamp is None:
            return True
        return True if (current_timestamp - generated_timestamp) > self.token_lifespan else False

    def get_token(self):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Retrieve the access token.')

        if (self.access_token is None):
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Access token expired or not present, generating a new one.')
            try:
                print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Send request to obtain the access token from cache service.')

                response = requests.post(system_config.DATASTORE_URL + '/generate-auth-token', \
                                    data={'username': system_config.DATASTORE_USR, 'password': system_config.DATASTORE_PSW}                
                                    )
            except:
                print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Access token error: Cannot connect to cache to get the access token, check connection or credentials.')

            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Register the token.')
            self.access_token = response.json()['auth-token']
            # self.token_lifespan = response.json()['result']['expire-interval'] - 20
            # self.generated_timestamp = datetime.now().timestamp()

        return self.access_token

access_token_manager = AccessToken()

def generate_request_validation(data):
    return all([key in ['user-id', 'generation-date', 'user-goal', 'user-level'] for key in data.keys()])

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Service {system_config.SCHEDULER_SERVICE_NAME} recieved request.')
    if generate_request_validation(dict(request.form)):

        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Start schedule generation.')
        new_population = gna_scheduler(generate_population(10, 10, request.form.get('user-level')), request.form.get('user-goal'))
        new_schedule = select_best_schedule(new_population, request.form.get('user-goal'))

        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Store data in cache.')
        response = requests.post(system_config.DATASTORE_URL + '/create', 
                     headers={'Authorization': access_token_manager.get_token()},
                     data={
                        'user-id': request.form.get('user-id'), 
                        'user-level': request.form.get('user-level'),
                        'goal' : request.form.get('user-goal'),
                        'schedule': list(new_schedule), 
                        'generation-date': request.form['generation-date']
                        })
        
        if response.status_code == 200:
            return {'message': f'Data stored for user {request.form.get("user-id")}.'}, 200
        return {'message': f'Cannot store data in datastore for user with user id{request.form.get("user-id")}.'}, 401
    return {'message': f'Bad request: Cannot validate the request for {request.form.get("user-id")}.'}, 401


def service_discovery_registration():
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Register service {system_config.SCHEDULER_SERVICE_NAME}.')

    config_json = {
        'service-name': system_config.SCHEDULER_SERVICE_NAME,
        'service-url': system_config.SCHEDULER_SERVICE_URL,
        'service-port': system_config.SCHEDULER_SERVICE_PORT,
        'service-endpoints': [path.rule for path in app.url_map._rules[1:]]
    }
    response = requests.post(system_config.SERVICE_DISCOVERY_URL, data=config_json)

    if response.status_code == 200:
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Service {system_config.SCHEDULER_SERVICE_NAME} registered successfully.')
    else:
        raise ValueError(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Service {system_config.SCHEDULER_SERVICE_NAME} could not be registered check service discovery url.')

if __name__ == "__main__":
    service_discovery_registration()

    app.run(host='0.0.0.0', port=system_config.SCHEDULER_SERVICE_PORT)