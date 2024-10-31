import sys
import os
import csv
from tabulate import tabulate # Library for a better visualization of the tables

connection_path = r"..\..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query

seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//instructor.csv"
cities_seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//instructor_cities.csv"
offering_seed_path = "..//..//database//dbt//dbt_snowflake_project//seeds//offering.csv"

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

def sign_in_instructor(name, phone_number):
    # Load connection
    connection = get_connection()
    
    # Check if the instructor exists in the database
    query = "SELECT * FROM instructor WHERE name = %s AND phoneNumber = %s"
    result = execute_query(connection, query, (name, phone_number))
    
    if result:
        instructor_data = result[0]  # Get the first matching row
        print(f"\nWelcome, {instructor_data[1]}!\n")  # Access by index
        # Return the object
        return True, {
            "instructor_id": instructor_data[0],
            "name": instructor_data[1],
            "phoneNumber": instructor_data[2],
            "specialization": instructor_data[3]
        }
    else:
        print("Did not work, try again!")
        return False, None  # Return False if not found
    

def view_available_offerings(instructor_id):
    connection = get_connection()
    
    # Step 1: Get cities where the instructor can work
    query_cities = """
        SELECT city_name 
        FROM instructor_cities 
        WHERE instructor_id = %s
    """
    cities_result = execute_query(connection, query_cities, (instructor_id,))
    cities = [f"'{row[0]}'" for row in cities_result]  # Format city names for SQL

    if not cities:
        print("There are no cities found where this instructor can work")
        return
    
    # Dynamically construct the IN clause
    cities_in_clause = ", ".join(cities)

    # Step 2: Get available offerings that match these cities and have NULL instructors
    query_offerings = f"""
        SELECT offering.offering_id, offering.type, location.name AS location_name, 
               offering.startDate, offering.endDate, offering.day, 
               offering.startTime, offering.endTime 
        FROM offering
        JOIN location ON offering.location = location.name
        WHERE location.city IN ({cities_in_clause}) AND offering.instructor IS NULL
    """
    offerings_result = execute_query(connection, query_offerings)

    # Display offerings if available
    if offerings_result:
        headers = ["Offering ID", "Type", "Location", "Start Date", "End Date", "Day", "Start Time", "End Time"]
        print(tabulate(offerings_result, headers=headers))
    else:
        print("No available offerings in the cities you can work in")


def take_offering(instructor_id, instructor_name):
    connection = get_connection()
    
    # Get the offerings the instructor can take 
    query_available_offerings = """
        SELECT offering.offering_id
        FROM offering
        JOIN location ON offering.location = location.name
        JOIN instructor_cities ON instructor_cities.city_name = location.city
        WHERE instructor_cities.instructor_id = %s AND offering.instructor IS NULL
    """
    available_offerings_result = execute_query(connection, query_available_offerings, (instructor_id,))
    available_offerings_ids = [row[0] for row in available_offerings_result]

    if not available_offerings_ids:
        print("No offerings available for you to take.")
        return
    
    # Ask instructor for the ID of the offering to take
    selected_offering_id = None
    try:
        selected_offering_id = int(input("Enter the ID of the offering you want to take: "))
    except ValueError:
        print("Invalid offering ID. Please enter a valid number")
        return
    
    # Check if the selected ID is in the list of available offerings
    if selected_offering_id not in available_offerings_ids:
        print("The selected offering is either unavailable or does not match your cities")
        return

    # Update the offering to set the instructor
    query_update_offering = """
        UPDATE offering
        SET instructor = %s
        WHERE offering_id = %s
    """
    execute_query(connection, query_update_offering, (instructor_name, selected_offering_id))
    
    print(f"Successfully taken offering with ID {selected_offering_id}.")

    # Add to the seed
    add_offering_seed(selected_offering_id, instructor_name)


def add_offering_seed(offering_id, instructor_name):
    temp_file_path = offering_seed_path + '.tmp'
    updated = False
    
    with open(offering_seed_path, mode='r', newline='') as file, open(temp_file_path, mode='w', newline='') as temp_file:
        reader = csv.reader(file)
        writer = csv.writer(temp_file)
        
        # Copy all rows and update only the selected offering_id row
        for row in reader:
            if row[0] == str(offering_id):  # Check if this row matches the offering_id
                row[-1] = instructor_name   # Update the instructor column
                updated = True
            writer.writerow(row)
    
    # Replace original file with the updated one
    os.replace(temp_file_path, offering_seed_path)
    return updated