import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//instructor.csv"
cities_seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//instructor_cities.csv"

def get_headers(table):
    # Define the path to the CSV file based on the table name
    seed_path = f"..//..//database//dbt//dbt_snowflake_project//seeds//{table}.csv"
    
    
    with open(seed_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Get the headers from the first row
        return headers
    
def get_last_ID(table):
    seed_path = f"..//..//database//dbt//dbt_snowflake_project//seeds//{table}.csv"
    last_seed_ID = None

    headers = get_headers(table)
    with open(seed_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_seed_ID = int(row[headers[0]])  # Get the last ID of the last row

    return last_seed_ID

def get_connection():
    file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    connection = load_profile(file_path) # Load the YAML profile file
    return connection

def add_into_instructor_seed(new_object):
    # Check if the file exists
    file_exists = os.path.exists(seed_path)

    with open(seed_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(["instructor_id", "name", "phoneNumber", "specialization"])
        
        # Append the new client data directly without adding a newline
        writer.writerow(new_object)  # Append the new client data

def add_into_instructor_cities_seed(new_object):

    file_exists = os.path.exists(cities_seed_path)

    with open(cities_seed_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new
        if not file_exists:
            writer.writerow(["instructor_cities_id","instructor_id","instructor", "city_name"])
        
        # Append the new client data directly without adding a newline
        writer.writerow(new_object)  # Append the new client data


def create_instructor_cities(instructor,connection,instructor_id):

    sentinel = True
    print("\nEnter the city(ies) where you can work or q to quit: ")
    city_count = 1

    while sentinel:
        city_name = input(f"Enter your {city_count} city: ")
        city_count = city_count + 1  # Increment the count to get the good order of the city
        instructor_cities_id = get_last_ID("instructor_cities") + 1

        if city_name != "q":
            insert_query = """
                    INSERT INTO instructor_cities (instructor_cities_id, instructor_id, instructor, city_name) 
                    VALUES (%s, %s, %s, %s);
                """
            execute_query(connection, insert_query, (instructor_cities_id,instructor_id, instructor, city_name))

            new_object = [instructor_cities_id, instructor_id,instructor, city_name]
            
            add_into_instructor_cities_seed(new_object)

        elif city_name == "q":
            sentinel = False
            break  #TO CHECK


def create_instructor():
    connection = get_connection()
    

    print("You have chosen to register as as intructor.\n")
    
    instructor_id = get_last_ID("instructor") + 1
    instructor_name = input("Enter your name: ")
    instructor_phone_number = input("Enter your phone number (###-###-####): ")
    instructor_specialization = input("Enter your specialization: ")

    insert_query = """
                INSERT INTO instructor (instructor_id, name, phoneNumber, specialization) 
                VALUES (%s, %s, %s, %s);
            """
    execute_query(connection, insert_query, (instructor_id, instructor_name, instructor_phone_number, instructor_specialization))

    new_object = [instructor_id, instructor_name, instructor_phone_number, instructor_specialization]
    add_into_instructor_seed(new_object)

    create_instructor_cities(instructor_name,connection,instructor_id)


