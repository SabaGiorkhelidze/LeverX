from mysql.connector import Error

class StudentInserter:
    @staticmethod
    def insert_students(students_data, db_connector):
        cursor = db_connector.cursor()
        
        try:
            for student in students_data:
                cursor.execute(
                    "INSERT IGNORE INTO students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)",
                    (student["id"], student["name"], student["sex"], student["birthday"], student["room"])
                )
            db_connector.commit()
        except Error as e:
            print(f"Error inserting students into db {e}")
        finally:
            cursor.close()
