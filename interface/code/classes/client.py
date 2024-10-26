import sys
import os
import csv

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
def client_register_message(client_age,):

    print("todo")


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




def test():
     new_object = [1, "Cristiano Ronaldo", 39, 'false', 'null']
     add_into_client_seed(new_object)