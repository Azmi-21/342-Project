import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

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

def view_data(table):
    connection = get_connection()
    select_query = f"SELECT * FROM {table}"  # Use the table parameter here
    results = execute_query(connection, select_query)

    # Check if there are any results
    if results:
        headers = get_headers(table)
        
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("No data to display")