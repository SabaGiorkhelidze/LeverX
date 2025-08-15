from dotenv import load_dotenv
import os

load_dotenv()

config = {
      'user': os.getenv('MYSQL_USER', 'User'),
      'password': os.getenv('MYSQL_PASSWORD', 'User123'),
      'host': os.getenv('MYSQL_HOST', 'localhost'),
      'database': os.getenv('MYSQL_DATABASE', 'Database'),
      'port': os.getenv('MYSQL_PORT', '3306'),
  }