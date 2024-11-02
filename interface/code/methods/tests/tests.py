import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables
from datetime import datetime

connection_path = r"..\..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    return connection

def check_existing_booking(client_id, offering_id):
    connection = get_connection()
    
    # Fetch the day and time of the requested offering
    query = "SELECT location, day, startTime, endTime FROM offering WHERE offering_id = %s"
    offering = execute_query(connection, query, (offering_id,))
    
    # Debug: Print the raw offering result
    #print(f"offering_id {offering_id}: {offering}")
    
    # Check if offering data was retrieved and properly formatted
    if not offering or len(offering[0]) < 4:
        print(f"Offering {offering_id} does not exist or has incomplete data.")
        return False


    location, offering_day, offering_start_time, offering_end_time = offering[0]
    
    # Check if the client already has a booking for the same day and time slot
    query = """
    SELECT b.booking_id
    FROM booking b
    JOIN offering o ON b.offering_id = o.offering_id
    WHERE b.client_id = %s
      AND o.day = %s
      AND (
          (%s >= o.startTime AND %s < o.endTime) OR
          (%s > o.startTime AND %s <= o.endTime) OR
          (o.startTime >= %s AND o.endTime <= %s)
      )
    """
    existing_booking = execute_query(connection, query, (client_id, offering_day, offering_start_time, offering_start_time, offering_end_time, offering_end_time, offering_start_time, offering_end_time))
    
    #print(f"client_id {client_id}, offering_id {offering_id}: {existing_booking}")
    
    if existing_booking:
        print(f"Client {client_id} already has a booking on {offering_day} from {offering_start_time} to {offering_end_time}.")
        return False
    
    return True