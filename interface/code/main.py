import sys
import os

connection_path = r"..\..\database\code"  # Ensure this points to the directory containing connection.py
sys.path.append(os.path.abspath(connection_path))

from connection import load_profile, execute_query
from classes.client import *

def main():

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