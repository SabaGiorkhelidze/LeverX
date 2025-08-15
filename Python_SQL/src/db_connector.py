from src.interfaces.interface import DatabaseConnectorInterface
import mysql.connector
from mysql.connector import Error

class DatabaseConnector(DatabaseConnectorInterface):
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connect()
        
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
        
        
    def cursor(self):
        return self.connection.cursor()
    
    def commit(self):
        self.connection.commit
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None