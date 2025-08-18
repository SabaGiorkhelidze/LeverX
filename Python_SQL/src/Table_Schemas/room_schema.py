from mysql.connector import Error



class RoomSchemaCreator:
    @staticmethod
    def create_room_table(cursor):
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL, 
                    INDEX idx_room_id (id)
                )
                """)
        except Error as e:
            print(f"Error creating room table: {e}")
            return
            