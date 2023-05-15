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
    SERVICE_DISCOVERY_URL = __get_environment_variable_str('SERVICE_DISCOVERY_URL', 'http://localhost:9050/get-services')
    
    # Datastore credentials for auth token generation
    DATASTORE_USR = __get_environment_variable_str('DATASTORE_USR', 'root')
    DATASTORE_PSW = __get_environment_variable_str('DATASTORE_PSW', '1234')
    DATASTORE_URL = __get_environment_variable_str('DATASTORE_URL', 'http://localhost:9060')

    MYSQL_USERNAME = __get_environment_variable_str('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = __get_environment_variable_str('MYSQL_PASSWORD', 'Test2023-mysql-pl-claim!')
    MYSQL_URL = __get_environment_variable_str('MYSQL_URL', 'localhost')
    MYSQL_PORT = __get_environment_variable_int('MYSQL_PORT', 3306)
    MYSQL_DBNAME = __get_environment_variable_str('MYSQL_DBNAME', 'fitnessapp')

    # GATEWAY_SERVICE_NAME = __get_environment_variable_str('GATEWAY_SERVICE_NAME', 'GNA-scheduler-1')
    GATEWAY_SERVICE_PORT = __get_environment_variable_int('GATEWAY_SERVICE_PORT', 9040)

system_config = SystemConfig()


    