from mysql.connector import Error
from interface import DatabaseConnectorInetrface

class StudentSchemaCreator:
    @staticmethod
    def create_student_table(cursor):
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    sex CHAR(1) NOT NULL,
                    birthday DATE NOT NULL,
                    room_id INT,
                    FOREIGN KEY (room_id) REFERENCES rooms(id)
                )
            """)
        except Error as e:
            print(f"Error creating students table: {e}")
            raise