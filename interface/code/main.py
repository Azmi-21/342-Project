import sys
import os

connection_path = r"..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

def main():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Updated path to YAML profile file
    query = "SELECT * FROM removeme;"
    execute_query(connection, query)

# Run the script
if __name__ == '__main__':
    main()