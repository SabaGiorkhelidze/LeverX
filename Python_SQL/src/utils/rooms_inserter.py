from mysql.connector import Error

class RoomInserter:
    @staticmethod
    def insert_rooms(self, rooms_data, db_connector):
        cursor = db_connector.cursor()
        
        try:
            for room in rooms_data:
                cursor.execute(
                    "INSERT IGNORE INTO rooms (id, name) VALUES (%s, %s)",
                    (room["id"], room["name"])
                )
                db_connector.commit()
        except Error as e:
            print(f"Error inserting rooms into db {e}")
        finally:
            cursor.close()