import sys
import os

connection_path = r"..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query
from classes.client import * 
from methods.view_data import *
from methods.delete_data import *

def main():

    sentinel = True
    while sentinel:
        print("\n")
        print("==========================================================")
        print("Welcome to the system. Please choose the options:")
        print("==========================================================\n")
        print("1: Sign in as Administrator")
        print("2: Register as a Client")
        print("3. Register as an Intructor")
        print("8: Local Testing")
        print("9: Exit")

        user_input = input("Enter your choice: ")

        if user_input == "1":
            password = input("Enter the password of admin account: ")

            if password == "admin":
                sentinel_admin = True

                while sentinel_admin:
                    print("")
                    print("1: View")
                    print("2: Delete")
                    print("8: Local Testing")
                    print("9: Go Back")
                    print("")
                    admin_input = input("Enter your choice: ")

                    if admin_input == "1":
                        print("1: Client")
                        print("2: Location")
                        print("3: Instructors")
                        print("8: Local Testing")
                        print("9: Go Back")
                        admin_input_1 = int(input("Which data you want to view: "))

                        # Defining the hashmapping to map user input with the tables
                        hash_input_tables = {1: "client", 2:"location", 3:"instructor", 4:"offering", 5:"booking"}
                        
                        # Iterate over each tables to get the good tabel
                        for i in hash_input_tables:
                            if admin_input_1 == i:
                                # View the data of selected table
                                view_data(hash_input_tables[i])

                    elif admin_input == "2":
                        print("1: Client")
                        print("2: Instructor")
                        print("8: Local Testing")
                        print("9: Go Back")
                        admin_input_2 = int(input("Which data you want to delete: "))

                        hash_input_2_tables = {1: "client", 2:"instructor"}

                        for i in hash_input_2_tables:

                            if admin_input_2 == i:
                                client_id = input("Enter client ID that you want to delete: ")
                                # Delete the row from selected table
                                delete_record(hash_input_2_tables[i],client_id)
                            

                    elif admin_input == "9":
                        sentinel_admin = False
            else:
                print("Wrong Password")

                

        elif user_input == "2":

            create_client()
       
        elif user_input == "8":
            test()

        elif user_input == "9":
            print("Exiting the system.")
            sentinel = False  # Exit the loop

# Run the script
if __name__ == '__main__':
    main()