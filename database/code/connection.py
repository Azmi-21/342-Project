import yaml
import snowflake.connector

import os

def load_profile(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile not found at {file_path}")
    with open(file_path, 'r') as file:
        profile = yaml.safe_load(file)
    return profile['dbt_snowflake_project']['outputs']['dev']


def execute_query(profile, query):
    # Establish connection
    conn = snowflake.connector.connect(
        account=profile['account'],
        user=profile['user'],
        password=profile['password'],
        database=profile['database'],
        schema=profile['schema'],
        warehouse=profile['warehouse'],
        role=profile['role']
    )
    
    # Execute the query
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    finally:
        cursor.close()
        conn.close()

# Define main function
def main():
    file_path = "..//dbt//dbt_snowflake_project//profiles.yml"
    profile = load_profile(file_path)  # Updated path to YAML profile file
    query = "SELECT * FROM removeme;"
    execute_query(profile, query)

# Run the script
if __name__ == '__main__':
    main()