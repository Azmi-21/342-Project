import sys
import os
import csv

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query


def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    return connection

def get_headers(table):
    # Define the path to the CSV file based on the table name
    seed_path = f"..//..//database//dbt//dbt_snowflake_project//seeds//{table}.csv"
    
    
    with open(seed_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Get the headers from the first row
        return headers
    
def delete_record(table,id):
    # Define the path to the CSV file based on the table name
    seed_path = f"..//..//database//dbt//dbt_snowflake_project//seeds//{table}.csv"

    with open(seed_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert to list for easier handling
    
    # Check if data has rows and headers
    if not data or len(data) <= 1:
        print("No data to delete.")
        return

    headers = data[0]
    rows = [row for row in data[1:] if row[0] != str(id)]  # Exclude rows with the given client_id

    # Write the updated data back to the file
    with open(seed_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write remaining rows

    headers = get_headers(table)
    id_column = headers[0]

    # Delete the object in Snowflake database
    connection = get_connection()
    delete_query = f"DELETE FROM {table} WHERE {id_column} = %s;"
    execute_query(connection, delete_query, (id,))

    print(f"Client with ID {id} has been deleted.")