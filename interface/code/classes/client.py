import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query


seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//client.csv"
underage_client_seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//underage_client.csv"

def get_last_ID():

    last_seed_ID = None
    with open(seed_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_seed_ID = int(row['client_id'])  # Get the last ID of the last row

    return last_seed_ID

def get_last_underage_client_ID():

    last_seed_ID = None
    with open(underage_client_seed_path , mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_seed_ID = int(row['underage_client_id'])  # Get the last ID of the last row

    return last_seed_ID

def add_into_client_seed(new_object):
    # Check if the file exists
    file_exists = os.path.exists(seed_path)

    with open(seed_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(['client_id', 'name', 'age', 'guardian'])
        
        # Append the new client data directly without adding a newline
        writer.writerow(new_object)  # Append the new client data

def add_into_underage_client_seed(new_object):
    file_exists = os.path.exists(underage_client_seed_path )

    with open(underage_client_seed_path , mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(['underage_client_id', 'cleint_name', 'age', 'guardian', 'relation'])
        
        # Append the new client data directly without adding a newline
        writer.writerow(new_object)  # Append the new client data

def client_register_message(client_name):

    print(f"{client_name} registered with the system.")

def client_guradian_register_message(guardian_name,underage_client_name,client_age,relation_client_guardian):

    print(f"{guardian_name} registered with the system for his/her {relation_client_guardian} {underage_client_name} (who is {client_age}).")

def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    return connection

def create_client():

    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path)  # Load the YAML profile file
    
    underage_client_name = None

    print("You have chosen to register as a client.\n")
    
    client_age = int(input("Enter your age: "))
    # Add the guardian if the client is underage
    if client_age < 18:

        guardian_age = None
        sentinel = True

        while(sentinel):
            guardian_age = int(input("How old is your guardian: "))

            if guardian_age < 18:
                print("The guardian is not valid. Please enter the age of the valid guardian: ")
            
            else:
                sentinel = False

        underage_client_id = get_last_underage_client_ID() + 1
        
        underage_client_name = input("Enter your name: ")
        guardian_name = input("Who is your guardian: ")
        guardian = "true"

       


        relation_client_guardian = input("What is your relation with your guardian: ")
        client_id = get_last_ID() + 1
        
        insert_query = """
                INSERT INTO client (client_id, name, age, guardian) 
                VALUES (%s, %s, %s, %s);
            """
        execute_query(connection, insert_query, (client_id, guardian_name, guardian_age, guardian))

        new_object = [client_id, guardian_name, guardian_age, guardian]
        #print(new_object)
        add_into_client_seed(new_object)


        insert_query = """
                INSERT INTO underage_client (underage_client_id, client_name,age, guardian, relation) 
                VALUES (%s, %s, %s, %s, %s);
            """
        execute_query(connection, insert_query, (underage_client_id, underage_client_name, client_age, guardian_name, relation_client_guardian))
        new_underage_client_object = [underage_client_id, underage_client_name, client_age, guardian_name, relation_client_guardian] 
        add_into_underage_client_seed( new_underage_client_object)

        client_guradian_register_message(guardian_name,underage_client_name,client_age,relation_client_guardian)

    else:

        client_name = input("Enter your name: ")

        # Set the client_id as appropriate (e.g., fetching the next id from the database)
        client_id = get_last_ID() + 1
        client_guardian = "false"
        
        insert_query = """
                INSERT INTO client (client_id, name, age, guardian) 
                VALUES (%s, %s, %s, %s);
            """
        execute_query(connection, insert_query, (client_id, client_name, client_age, client_guardian))

        new_object = [client_id, client_name, client_age, client_guardian]
        #print(new_object)
        add_into_client_seed(new_object)

        client_register_message(client_name)

def view_client_data():

    connection = get_connection()
    select_query = "select * from client"
    results = execute_query(connection, select_query)

    # Check if there are any results
    if results:
        headers = ["client_id", "name", "age", "guardian"]  # Update headers if column names change
        print(tabulate(results, headers=headers, tablefmt="grid"))
    else:
        print("No data to display")
        

def delete_client_record(client_id):

    with open(seed_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert to list for easier handling
    
    # Check if data has rows and headers
    if not data or len(data) <= 1:
        print("No data to delete.")
        return

    headers = data[0]
    rows = [row for row in data[1:] if row[0] != str(client_id)]  # Exclude rows with the given client_id

    # Write the updated data back to the file
    with open(seed_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write remaining rows

    # Delete the object in Snowflake database
    connection = get_connection()
    delete_query = "DELETE FROM client WHERE client_id = %s;"
    execute_query(connection, delete_query, (client_id,))

    print(f"Client with ID {client_id} has been deleted.")

def test():
     new_object = [1, "Cristiano Ronaldo", 39, 'false', 'null']
     add_into_client_seed(new_object)