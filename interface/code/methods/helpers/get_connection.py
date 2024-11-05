import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    return connection