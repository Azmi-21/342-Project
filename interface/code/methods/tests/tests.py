import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query


def check_time_slot_conflict(connection, location, day, start_time, end_time):
    
    # Check if the given time slot for a specified location and day overlaps with any existing offerings.
    query = """
    SELECT * FROM offering
    WHERE location = %s AND day = %s AND (
        (%s >= startTime AND %s < endTime) OR
        (%s > startTime AND %s <= endTime) OR
        (startTime >= %s AND endTime <= %s)
    )
    """
    results = execute_query(connection, query, (location, day, start_time, start_time, end_time, end_time, start_time, end_time))
    
    if results:
        return True  # Conflict found
    return False  # No conflict