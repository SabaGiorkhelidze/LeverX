import json
from src.config import config
from src.db_connector import DatabaseConnector
from src.schema import SchemaCreator
from src.data_inserter import DataInserter
from src.query import QueryExecutor
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  
ROOMS_FILE = BASE_DIR / 'jsons' / 'rooms.json'
STUDENTS_FILE = BASE_DIR / 'jsons' / 'students.json'

def run_app():
    
    db  = DatabaseConnector(config)
    
    schema_creator = SchemaCreator(db)
    schema_creator.create_db()
    
    db = DatabaseConnector(config)
    
    with open(ROOMS_FILE, 'r') as f:
        rooms_data = json.load(f)

    with open(STUDENTS_FILE, 'r') as f:
        students_data = json.load(f)
        
    inserter = DataInserter(db)
    inserter.insert_rooms(rooms_data)
    inserter.insert_students(students_data)
    
    
    executor = QueryExecutor(db)
    
    print("Rooms with student count:")
    print(executor.get_rooms_with_student_count())
    
    print("\nTop 5 rooms with smallest average student age:")
    print(executor.get_top_5_rooms_smallest_avg_age())
    
    print("\nTop 5 rooms with largest age difference:")
    print(executor.get_top_5_rooms_largest_age_diff())
    
    print("\nRooms with mixed sexes:")
    print(executor.get_rooms_with_mixed_sexes())
    
    db.close_connection()
    

if __name__ == "__main__":
    run_app()