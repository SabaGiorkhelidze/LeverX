from mysql.connector import Error
from src.interfaces.interface import SchemaCreatorInterface, DatabaseConnectorInterface
from src.Table_Schemas.room_schema import RoomSchemaCreator
from src.Table_Schemas.student_schema import StudentSchemaCreator
from src.config import config

class SchemaCreator(SchemaCreatorInterface):
    def __init__(self, db_connector: DatabaseConnectorInterface):
        self.db =  db_connector
    
    
    def create_db(self):
        cursor = self.db.cursor()
        
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config['database']}`")  # Use backticks for safety
            cursor.execute(f"USE `{config['database']}`")  # Use the same database name
            RoomSchemaCreator.create_room_table(cursor)
            StudentSchemaCreator.create_student_table(cursor)
            self.db.commit()
        except Error as e:
            print(f"Error creating schema: {e}")
            raise
        finally:
            cursor.close()