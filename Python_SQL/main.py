# main.py
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.app import run_app

print("run")
try:
    run_app()
except Exception as e:
    print(f"Error: {e}")