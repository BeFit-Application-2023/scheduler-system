import mysql
import requests
from mysql.connector import Error
from datetime import datetime


class MySQLQuery:
    def __init__(self, host, username, password, db_name) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name

        self.connection = self.connect()

    def connect(self):
        connection = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                database=self.db_name
            )
            print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Connection to MySQL database established.')
        except Error as err:
            print(f'{datetime.now().strftime("%H:%M:%S")} [ERROR] {err}')

        return connection

    def query(self, query_command):
        cursor = self.connection.cursor()
        result = None

        try:
            # print(f'{datetime.now().strftime("%H:%M:%S")} [INFO] Query MySQL database with the provided string.')
            cursor.execute(query_command)
            result = cursor.fetchall()

            return result
        except Error as err:
            print(f"Error: '{err}'")