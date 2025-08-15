from mysql.connector import Error
from src.interfaces.interface import DatabaseConnectorInterface


class RoomSchemaCreator:
    @staticmethod
    def create_room_table(cursor):
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL 
                )
                """)
        except Error as e:
            print(f"Error creating room table: {e}")
            return
            