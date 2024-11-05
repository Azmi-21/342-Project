import yaml
import snowflake.connector

import os

def load_profile(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile not found at {file_path}")
    with open(file_path, 'r') as file:
        profile = yaml.safe_load(file)
    return profile['dbt_snowflake_project']['outputs']['dev']


def execute_query(profile, query, params=None):
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
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Check if it's a SELECT query to fetch and return data
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()  # Fetch all results for SELECT
        else:
            results = None  # For non-SELECT queries, nothing to return
            conn.commit()   # Commit changes for INSERT, UPDATE, DELETE
        return results

    finally:
        cursor.close()
        conn.close()