## Setup
1. Ensure MySQL is installed and running on `localhost:3306`.
2. Create a `.env` file in the root directory with:
   ```
   MYSQL_USER="{{user}}"
   MYSQL_PASSWORD="{{password}}"
   MYSQL_HOST="localhost"
   MYSQL_DATABASE="{{db_name}}"
   MYSQL_PORT="{{port}} | 3306"
   MYSQL_ROOT_PASSWORD="{{root_password}}"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure `jsons/rooms.json` and `jsons/students.json` exist with valid data.

## Running the Project
- Navigate to the project root (`Python_SQL`).
- Run:
  ```bash
  python main.py
  ```

## Notes
- Grant MySQL privileges to {{User}} with:
  ```sql
  GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost' IDENTIFIED BY 'user';
  FLUSH PRIVILEGES;
  ```