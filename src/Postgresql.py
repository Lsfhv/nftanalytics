import psycopg2
import os

class PostgresConnection:
    """
    Returns a connection to the postgres db.
    """
    def __init__(self):
        self.host = os.environ['PGSQLHOST']
        self.port = os.environ['PGSQLPORT']
        self.user = os.environ['USER']
        self.db = os.environ['PGSQLDB']

        self.connection = self.connect()

    def connect(self):
        connection = psycopg2.connect(database=self.db, user=self.user, password='', host=self.host, port=self.port)
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