from mysql.connector import Error
from src.utils.rooms_inserter import RoomInserter
from src.utils.students_inserter import StudentInserter

class DataInserter:
    def __init__(self, db_connector):
        self.db = db_connector
        
    def insert_rooms(self,  rooms_data):
        try:
            RoomInserter.insert_rooms(rooms_data, self.db)
        except Error as e:
            print(f"Error in insert_rooms: {e}")
            raise
    
    def insert_students(self, students_data):
        try:
            StudentInserter.insert_students(students_data, self.db)
        except Error as e:
            print(f"Error in insert_students: {e}")
            raise