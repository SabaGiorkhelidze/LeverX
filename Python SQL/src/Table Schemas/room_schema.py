from mysql.connector import Error
from interface import DatabaseConnectorInetrface


class RoomSchemaCreator:
    @staticmethod
    def create_room_schema(cursor):
        try:
            cursor.execute("""  """)
        except Error as e:
            print(e)
            return
            