import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query


def add_row_to_seed(seed_file_path,temp_file_path,column_name,row_id,new_value):
    with open(seed_file_path, mode='r', newline='') as file, open(temp_file_path, mode='w', newline='') as temp_file:
        reader = csv.reader(file)
        writer = csv.writer(temp_file)
        
        headers = next(reader)  
        writer.writerow(headers)  
        
        if column_name in headers:
            column_index = headers.index(column_name)  
            
           
            for row in reader:
                if row[0] == str(row_id):  # Check if this row matches the row_id
                    row[column_index] = new_value  # Update the specific column
                    updated = True
                writer.writerow(row)
    
    # Replace original file with the updated one if an update occurred
    if updated:
        os.replace(temp_file_path, seed_file_path)
    else:
        os.remove(temp_file_path)  # Clean up if no update was made

    return updated