from mysql.connector import Error
from interface import SchemaCreatorInterface, DatabaseConnectorInetrface


'''
create table 

'''

class SchemaCreator(SchemaCreatorInterface):
    def __init__(self, db_connector: DatabaseConnectorInetrface):
        self.db =  db_connector
    
    
    def create_db(self):
        cursor = self.db.cursor()
        
        try:
            pass  
        except:
            pass