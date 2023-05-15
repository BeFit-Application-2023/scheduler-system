import os
from datetime import datetime


class SystemConfig:

    # @staticmethod
    def __get_environment_variable_str(ENV_NAME, DEFAULT_VALUE):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Get environment variable {ENV_NAME} value.')
        ENV_VAR = os.environ.get(ENV_NAME)
        
        if ENV_VAR:
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is present with value {ENV_VAR}')
            return ENV_VAR
        
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is missing using the default value {DEFAULT_VALUE}')
        return DEFAULT_VALUE
    
    # @staticmethod
    def __get_environment_variable_int(ENV_NAME, DEFAULT_VALUE):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Get environment variable {ENV_NAME} value.')

        ENV_VAR = os.environ.get(ENV_NAME)

        if ENV_VAR:
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is present with value {ENV_VAR}')
            return int(ENV_VAR)
        
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is missing using the default value {DEFAULT_VALUE}')
        return DEFAULT_VALUE

    # Service discovery url
    SERVICE_DISCOVERY_URL = __get_environment_variable_str('SERVICE_DISCOVERY_URL', 'http://localhost:9050/register')
    
    # Datastore credentials for auth token generation
    DATASTORE_USR = __get_environment_variable_str('DATASTORE_USR', 'root')
    DATASTORE_PSW = __get_environment_variable_str('DATASTORE_PSW', '1234')
    DATASTORE_URL = __get_environment_variable_str('DATASTORE_URL', 'http://localhost:9060')

    SCHEDULER_SERVICE_NAME = __get_environment_variable_str('SCHEDULER_SERVICE_NAME', 'GNA-scheduler-1')
    SCHEDULER_SERVICE_URL = __get_environment_variable_str('SCHEDULER_SERVICE_URL', 'http://127.0.0.1')
    SCHEDULER_SERVICE_PORT = __get_environment_variable_int('SCHEDULER_SERVICE_PORT', 6000)

system_config = SystemConfig()


    