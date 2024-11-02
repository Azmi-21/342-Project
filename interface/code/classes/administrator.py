import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

offering_seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//offering.csv"

def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    return connection


def get_last_ID():

    last_seed_ID = None
    with open(offering_seed_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_seed_ID = int(row['offering_id'])  # Get the last ID of the last row

    return last_seed_ID

def add_into_offering_seed(new_offering):
    file_exists = os.path.exists(offering_seed_path)
    
    with open(offering_seed_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(["offering_id", "type", "location", "startDate", "endDate", "day", "startTime", "endTime", "instructor"])
        
        # Write the new offering
        writer.writerow(new_offering)

def create_offering():

    connection = get_connection()
    # Prompt for offering details
    offering_id = get_last_ID() + 1
    offering_type = input("Enter the type of offering (e.g., 'Private' or 'Group'): ")
    location = input("Enter the location of the offering (e.g., 'Aquatic Center'): ")
    start_date = input("Enter the start date (DD-MM-YYYY): ")
    end_date = input("Enter the end date (DD-MM-YYYY): ")
    day = input("Enter the day of the week (e.g., 'Sunday'): ")
    start_time = input("Enter the start time (HH:MM): ")
    end_time = input("Enter the end time (HH:MM): ")
    status = "Available"

    query = """
    INSERT INTO offering (offering_id, type, location, startDate, endDate, day, startTime, endTime, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
    """

    execute_query(connection,query, (offering_id,offering_type, location, start_date, end_date, day, start_time, end_time, status))

    # Add the new object  to the seed
    new_offering = [offering_id, offering_type, location, start_date, end_date, day, start_time, end_time, "", status] # Empty string to have a null value for the instructor
    add_into_offering_seed(new_offering)

