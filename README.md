# 342 project: ClassConnect

## Introduction
**ClassConnect** is a scheduling and booking system designed to help organizations offer private and group lessons. It allows administrators to manage lesson offerings, instructors to register and accept available sessions, and clients to browse and book lessons. The system supports multiple lesson types, varying time slots, and allows legal guardians to manage bookings for underage clients.

## Installation

**Note**: The system only works on windows
### dbt profile
- Set up your dbt profile to make the connection to snowflake in `dbt_snowflake_project` folder
### Virtual Environment
- Change the directory:  `cd .\342-Project\virtual_env\`

#### Windows
- Install the libraries: `.\windows_setup.bat`
- Activate the virtual environment: `soen342project-env\Scripts\activate`

### Running the file
- Change the directory: `cd ../interface/code/`

#### Windows
- Run the file: `python main.py`



## UML Use case diagram
![Use case diagram 342](https://github.com/user-attachments/assets/652978ee-4cb5-45ee-a393-5876ac71983e)

## Technologies Used
- **Programming Language**: Python
- **UML Tools**: Lucidchart
- **Version Control**: GIT,GitHub
- **Database**: Snowflake

## Team Members
- **Azmi Abidi**, ID: 40248132
- **Alimurat Dinchdonmez**, ID: 40245310
