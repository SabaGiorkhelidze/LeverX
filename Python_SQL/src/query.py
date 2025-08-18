from mysql.connector import Error


class QueryExecutor:
    def __init__(self, db_connector):
        self.db = db_connector
          
    def _execute_query(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()
            
            
    def get_room_with_student_count(self):
        query = """
            SELECT r.name, COUNT(s.id) as student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room_id
            GROUP BY r.name
        """
        return self._execute_query(query)
    
    def get_top_5_rooms_smallest_avg_age(self):
        query = """
            SELECT r.name, AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.name
            HAVING COUNT(s.id) > 0
            ORDER BY avg_age ASC
            LIMIT 5
        """
        return self._execute_query(query)

    def get_top_5_rooms_largest_age_diff(self):
        query = """
            SELECT r.name, MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) as age_diff
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.name
            HAVING COUNT(s.id) > 1
            ORDER BY age_diff DESC
            LIMIT 5
        """
        return self._execute_query(query)

    def get_rooms_with_mixed_sexes(self):
        query = """
            SELECT r.name
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.name
            HAVING COUNT(DISTINCT s.sex) > 1
        """
        return self._execute_query(query)