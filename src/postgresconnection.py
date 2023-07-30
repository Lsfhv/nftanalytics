import psycopg2

from src.postgresconfig import *

class PostgresConnection:
    def __init__(self):
        self.host = host
        self.port = port
        self.user = user
        self.db = db

        self.connection = self.connect()

    def connect(self):
        connection = psycopg2.connect(database=self.db, user=self.user, password='', host=self.host, port=self.port)
        return connection
    
    def execute(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

        return "Done"
    
    def readonly(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)

        return cursor.fetchall()