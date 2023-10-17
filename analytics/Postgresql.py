import psycopg2
import os

class PostgresConnection:
    """
    Returns a connection to the postgres db.
    """
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '5432'
        self.user = 'postgres'
        self.db = 'nftanalytics'

        self.connection = self.connect()

    def connect(self):
        connection = psycopg2.connect(database=self.db, user=self.user, password='x', host=self.host, port=self.port)
        return connection
    
    def insert(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

        return "Done"
    
    """
    Execute commands like select.
    """
    def readonly(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        
        return cursor.fetchall()