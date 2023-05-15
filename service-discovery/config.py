import os
from datetime import datetime


class SystemConfig:

    def __get_environment_variable_str(ENV_NAME, DEFAULT_VALUE):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Get environment variable {ENV_NAME} value.')
        ENV_VAR = os.environ.get(ENV_NAME)
        
        if ENV_VAR:
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is present with value {ENV_VAR}')
            return ENV_VAR
        
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is missing using the default value {ENV_VAR}')
        return DEFAULT_VALUE
    
    def __get_environment_variable_int(ENV_NAME, DEFAULT_VALUE):
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Get environment variable {ENV_NAME} value.')

        ENV_VAR = os.environ.get(ENV_NAME)

        if ENV_VAR:
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is present with value {ENV_VAR}')
            return int(ENV_VAR)
        
        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Environment variable "{ENV_NAME}" is missing using the default value {ENV_VAR}')
        return DEFAULT_VALUE

    # Service discovery url
    SERVICE_DISCOVERY_URL = __get_environment_variable_str('SERVICE_DISCOVERY_URL', 'http://localhost')
    SERVICE_DISCOVERY_PORT = __get_environment_variable_int('SERVICE_DISCOVERY_PORT', 9050)

system_config = SystemConfig()


    