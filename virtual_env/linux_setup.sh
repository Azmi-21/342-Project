# Initialize the virtual environment
python3 -m venv soen342project-env


# Activate the virtual environment
source soen342project-env/bin/activate


# Installing DBT
python3 -m pip install dbt-core
python3 -m pip install dbt-snowflake


# Installing Python Libraries
python3 -m pip install pyyaml
python3 -m pip install snowflake-connector-python
python3 -m pip install tabulate