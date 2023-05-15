import json
import hashlib
import requests
from config import system_config
from datetime import datetime


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
                print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Send request to obtain the access token from cache.')

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

def generate_request_validation(data):
    return all([key in ['user-id', 'generation-date', 'user-goal', 'user-level'] for key in data.keys()])

def read_request_validation(data):
    return all([key in ['user-id', 'generation-date'] for key in data.keys()])

def check_service_presence(gateway_service_mapper, services_information):
    return list(filter(lambda x: x not in gateway_service_mapper.keys(), services_information.keys()))

class ConsistencyHashing:
    
    def __init__(self) -> None:
        self.nodes = []
        self.node_coordinates = []

    def register_node(self, new_node):
        self.nodes.append(new_node)
        base_step = 359 // len(self.nodes)
        self.node_coordinates = [base_step * idx for idx in range(len(self.nodes))]

    def estimate_distance(self, coordinate_a, coordinate_b):
        return abs(coordinate_a - coordinate_b)

    def estimate_nearest_neighbour(self, user_data):
        if self.nodes:

            user_data_coordinate = hash(str(user_data)) % 359
            candidates = [self.estimate_distance(user_data_coordinate, node_coordinate) for node_coordinate in self.node_coordinates]
            idx_candidate = candidates.index(max(candidates))

            return self.nodes[idx_candidate]
        
        return None


