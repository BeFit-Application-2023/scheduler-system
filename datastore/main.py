import threading
from uuid import uuid4
from datetime import datetime

import mysql
from flask import Flask, request, jsonify
from config import system_config
from db_connector import MySQLQuery
from datetime import datetime

app = Flask(__name__)

global_lock = threading.Lock()
mysql_connector = MySQLQuery(host=system_config.MYSQL_URL, username=system_config.MYSQL_USERNAME, 
                             password=system_config.MYSQL_PASSWORD, db_name=system_config.MYSQL_DBNAME)

# mysql_connector_read = MySQLQuery(host=system_config.MYSQL_URL, username=system_config.MYSQL_USERNAME, 
#                              password=system_config.MYSQL_PASSWORD, db_name=system_config.MYSQL_DBNAME)

GENERATED_AUTH_TOKENS = []

@app.route('/generate-auth-token', methods=['POST'])
def generate_auth_token():
    print(request.form)
    print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Recieved request for authentication token generation.')
    if ('username' in request.form.keys()) and ('password' in request.form.keys()):

        print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Check provided credentials.')
        if (request.form['username'] == system_config.DATASTORE_USERNAME) and (request.form['password'] == system_config.DATASTORE_PASSWORD):
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Token generation.')
            auth_token = uuid4()
            GENERATED_AUTH_TOKENS.append(str(auth_token))
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Send back the request containing the newly generated token.')
            return {'message': 'Authentication token generated.', 'auth-token': auth_token}, 200
        
        print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] Unauthorized access, provided credentials does not match.')
        return {'message': 'The credentials are not provided.', 'auth-token': None}, 401

    print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] Bad request, the request does not contain the keys for extracting the credentials.')
    return {'message': 'The credentials are not provided.', 'auth-token': None}, 400


@app.route('/create', methods=['POST'])
def create():
    print(f'{datetime.now().strftime("%H:%M:%S")} [CREATE] Recieved request.')

    if str(request.headers['Authorization']) in GENERATED_AUTH_TOKENS:
        schedule = request.form.getlist('schedule')
        print(request.form)
        create_query = f"""INSERT INTO schedulercache.generatedschedules 
            (user_id, datetime, schedule_element_1, schedule_element_2, schedule_element_3, schedule_element_4, schedule_element_5, 
            schedule_element_6, schedule_element_7, schedule_element_8, schedule_element_9, schedule_element_10) 
            VALUES 
            ({request.form.get('user-id')}, 
            '{request.form.get('generation-date')}', 
            '{schedule[0]}',
            '{schedule[1]}',
            '{schedule[2]}',  
            '{schedule[3]}',
            '{schedule[4]}',
            '{schedule[5]}',  
            '{schedule[6]}',
            '{schedule[7]}',
            '{schedule[8]}',  
            '{schedule[9]}' 
            );"""
        try:
            global_lock.acquire()
            mysql_connector.query(create_query)
            mysql_connector.connection.commit()
            global_lock.release()
        except:
            print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot insert to database.')

        return {'message': f'Data inserted for user {request.form.get("user-id")}'}, 200
    return {'message': f'Unauthorized access, authentication token is not present or is expired.'}, 301


@app.route('/read', methods=['POST'])
def read():
    # print(GENERATED_AUTH_TOKENS)
    # print(str(request.headers['Authorization']))
    print(f'{datetime.now().strftime("%H:%M:%S")} [READ] Recieved request to read from cache.')
    if str(request.headers['Authorization']) in GENERATED_AUTH_TOKENS:

        create_query = f"""
            SELECT * FROM schedulercache.generatedschedules 
            WHERE user_id = {request.form.get('user-id')} AND `datetime` = '{request.form.get('generation-date')}';
        );
        """
        # result = mysql_connector_read.query(create_query)

        # return {'user-data': list(result[0]), 'user-id': request.form.get('user-id'), 
        #         'generation-date': request.form.get('generation-date')}, 200
        try:
            global_lock.acquire()
            result = mysql_connector.query(create_query)
            global_lock.release()

            return {'user-data': list(result[0]), 'user-id': request.form.get('user-id'), 
                    'generation-date': request.form.get('generation-date')}, 200
        except mysql.connector.errors.OperationalError as ex:
            print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] Cannot establish the connection MySQL database.')

        except:
            print(f'{datetime.now().strftime("%H:%M:%S")} [WARN] Schedule not generated yet, for user {request.form.get("user-id")}.')

        return {'message': f'Schedule not generated yet, for user {request.form.get("user-id")}'}, 202
    return {'message': f'Unauthorized access, authentication token is not present or is expired.'}, 301


@app.route('/query', methods=['POST'])
def query():
    pass


@app.route('/delete', methods=['POST'])
def delete():
    pass


if __name__ == "__main__":
    app.run('0.0.0.0', port=system_config.DATASTORE_SERVICE_PORT)