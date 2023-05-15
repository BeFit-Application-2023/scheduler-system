import json
import threading
import requests
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from config import system_config
from utils import AccessToken, generate_request_validation, read_request_validation, ConsistencyHashing, check_service_presence
from service_utilities import Director
from queue import Queue


app = Flask(__name__)
director = Director()
SERVICE_MAPPER = {}

global_lock = threading.Lock()
user_queue = Queue()
access_token_manager = AccessToken()
consistency_hashing = ConsistencyHashing()


def get_available_services():
    global SERVICE_MAPPER

    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Attempt to retrieve the generation servies information from service discovery.')

    try:
        response = requests.post(system_config.SERVICE_DISCOVERY_URL, json={})
        if response.json():
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Recieved information about the available generation services, overwrite the current SERVICE_MAPPER.')
            response_json = response.json()

            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Check if there are new services registered.')
            new_services = check_service_presence(SERVICE_MAPPER, response_json)
            
            if new_services:
                for new_service in new_services:
                    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Detected a new service with name {new_service}.')
                    SERVICE_MAPPER[new_service] = response_json[new_service]

                    global_lock.acquire()
                    consistency_hashing.register_node(new_service)
                    global_lock.release()
    except:
        print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot retrieve service information from service discovery.')


def user_request_partitition():
    if not user_queue.empty():
        while not user_queue.empty():
            
            user_data = user_queue.get()

            global_lock.acquire()
            service_name = consistency_hashing.estimate_nearest_neighbour(user_data)
            global_lock.release()

            try:
                response = requests.post(SERVICE_MAPPER[service_name]['service-url'] + ':' + \
                                        SERVICE_MAPPER[service_name]['service-port'] + \
                                        SERVICE_MAPPER[service_name]['service-endpoints'], 
                                        data=user_data
                    )
                if response.status_code != 200:
                    user_queue.put(user_data)
            except:
                print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot connect to {service_name} for schedule generation.')
                print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] Reinsert the user data to queue.')

                user_queue.put(user_data)

background_scheduler = BackgroundScheduler(daemon=True)
background_scheduler.add_job(get_available_services, 'interval', seconds=5)
background_scheduler.add_job(user_request_partitition, 'interval', seconds=5)


@app.route('/read', methods=['POST'])
def read():
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Query request: {request.form}')
    if read_request_validation(dict(request.form)):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Request data from cache.')
        try:
            response = requests.post(system_config.DATASTORE_URL + '/read', 
                            headers={'Authorization': access_token_manager.get_token()},
                            data={
                                'user-id': request.form.get('user-id'), 
                                'generation-date': request.form.get('generation-date')
                            })
            
            if response.status_code == 202:
                return {'message': 'Processing, data is not ready yet.'}, 202
            
            if response.status_code == 200:
                return response.json(), 200
        except:
            print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot connect to cache to retrieve the schedules.')

        return {'message': 'Some error has occured'}, 401
        
    return {'message': 'Bad request, the fields does not match the template.'}, 401


@app.route('/generate', methods=['POST'])
def generate():
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Recieved request for generation.')
    if generate_request_validation(dict(request.form)):
        try:
            # response = requests.post(SERVICE_MAPPER[list(SERVICE_MAPPER.keys())[0]]['service-url'] + ':' + \
            #                         SERVICE_MAPPER[list(SERVICE_MAPPER.keys())[0]]['service-port'] + \
            #                         SERVICE_MAPPER[list(SERVICE_MAPPER.keys())[0]]['service-endpoints'], 
            #                         data={
            #                             'user-id': request.form['user-id'], 
            #                             'generation-date': request.form['generation-date'], 
            #                             'user-goal': request.form['user-goal'],
            #                             'user-level': request.form['user-level']
            #                             }
            #     )
            user_queue.put({
                'user-id': request.form['user-id'], 
                'generation-date': request.form['generation-date'], 
                'user-goal': request.form['user-goal'],
                'user-level': request.form['user-level']
            })
            return {'message': 'Accepted.'}, 200
        except:
            print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot connect to generation service.')
        
        # if response.status_code == 200:
        #     return {'message': 'Accepted.'}, 200
        return {'message': 'Something went wrong with inserting the user data to queue.'}, 401
    
    print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] Cannot validate the request.')
    return {'message': 'Bad request, check the request structure.'}, 401


if __name__ == "__main__":
    background_scheduler.start()
    app.run('0.0.0.0', port=system_config.GATEWAY_SERVICE_PORT, debug=True)