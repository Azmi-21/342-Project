import sys
import os

connection_path = r"..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query
from classes.client import create_client,test

def main():
    # file_path = "..//..//database//dbt//dbt_snowflake_project//profiles.yml"
    # connection = load_profile(file_path)  # Load the YAML profile file

    sentinel = True
    while sentinel:
        print("\n")
        print("==========================================================")
        print("Welcome to the system. Please choose the options:")
        print("==========================================================\n")
        print("1: Sign in as Administrator")
        print("2: Register as a client")
        print("8: Local Testing")
        print("9: Exit")

        user_input = input("Enter your choice: ")

        if user_input == "1":
            print("You have chosen to sign in as Administrator.")
            # TODO: Add your administrator logic here

        elif user_input == "2":
            create_client()
            # print("You have chosen to register as a client.\n")

            # client_name = input("Enter your name: ")
            # client_age = int(input("Enter your age: "))
            # isUnderage = 'true' if client_age < 18 else 'false'  # Set to 'true' if underage
            # client_guardian = None

            # # Add the guardian if the client is underage
            # if client_age < 18:
            #     client_guardian = input("Who is your guardian: ")

            # # Set the client_id as appropriate (e.g., fetching the next id from the database)
            # client_id = 3  # This should be generated based on your logic

            # insert_query = """
            #     INSERT INTO client (client_id, name, age, isUnderage, guardian) 
            #     VALUES (%s, %s, %s, %s, %s);
            # """
            # execute_query(connection, insert_query, (client_id, client_name, client_age, isUnderage, client_guardian))
        elif user_input == "8":
            test()

        elif user_input == "9":
            print("Exiting the system.")
            sentinel = False  # Exit the loop

# Run the script
if __name__ == '__main__':
    main()