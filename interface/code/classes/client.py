import sys
import os
import csv

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//client.csv"

def get_last_ID():

    last_seed_ID = None
    with open(seed_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_seed_ID = int(row['client_id'])  # Get the last ID of the last row

    return last_seed_ID


def add_into_client_seed(new_object):
    seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//client.csv"
    
    # Check if the file exists
    file_exists = os.path.exists(seed_path)

    with open(seed_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(['client_id', 'name', 'age', 'isUnderage', 'guardian'])
        
        # Append the new client data directly without adding a newline
        writer.writerow(new_object)  # Append the new client data

def create_client():

    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file

    print("You have chosen to register as a client.\n")
    
    client_name = input("Enter your name: ")
    client_age = int(input("Enter your age: "))
    isUnderage = 'true' if client_age < 18 else 'false'  # Set to 'true' if underage
    client_guardian = None

    # Add the guardian if the client is underage
    if client_age < 18:
        client_guardian = input("Who is your guardian: ")

    # Set the client_id as appropriate (e.g., fetching the next id from the database)
    client_id = get_last_ID() +1 # This should be generated based on your logic

    insert_query = """
            INSERT INTO client (client_id, name, age, isUnderage, guardian) 
            VALUES (%s, %s, %s, %s, %s);
        """
    execute_query(connection, insert_query, (client_id, client_name, client_age, isUnderage, client_guardian))

    new_object = [client_id, client_name, client_age, isUnderage, client_guardian]
    print(new_object)
    add_into_client_seed(new_object)

def test():
     new_object = [1, "Cristiano Ronaldo", 39, 'false', 'null']
     add_into_client_seed(new_object)