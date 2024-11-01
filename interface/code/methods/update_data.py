import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query
from methods.helpers.add_row_to_seed import *
from methods.helpers.get_connection import *

def update_data(table_name, row_id, column_name, new_value):

    connection = get_connection()
    # Define the path to the seed based on table name
    seed_file_path = os.path.join("..//..//database//dbt//dbt_snowflake_project//seeds//", f"{table_name}.csv")
    temp_file_path = seed_file_path + '.tmp'
    updated = False

    # Map table names to their CSV header columns
    seed_headers = {
        "client": ["client_id", "name", "age", "guardian"],
        "location": ["location_id", "name", "address"],
        "instructor": ["instructor_id", "name", "phoneNumber", "specialization"],
        "offering": ["offering_id", "type", "location", "startDate", "endDate", "day", "startTime", "endTime", "instructor"],
        "booking": ["booking_id","client_id","offering_id","bookingDate","startTime","endTime"],
        "instructor_cities": ["instructor_cities_id","instructor_id","instructor","city_name"],
        "underage_client": ["underage_client_id","client_name","age","guardian","relation"]
    }

    add_row_to_seed(seed_file_path,temp_file_path,column_name,row_id,new_value)

    query = f"UPDATE {table_name} SET {column_name} = %s WHERE {table_name}_id = %s"
    
    # Execute the query in Snowflake
    execute_query(connection,query, (new_value, row_id))
    print(f"Successfully updated {column_name} in {table_name} with ID {row_id}")