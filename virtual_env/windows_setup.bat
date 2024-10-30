@echo off
REM Initialize the virtual environment
python -m venv soen342project-env


REM Activate the virtual environment
call soen342project-env\Scripts\activate


REM Installing DBT
python -m pip install dbt-core
python -m pip install dbt-snowflake


REM Installing Python Libraries
python -m pip install pyyaml
python -m pip install snowflake-connector-python
python -m pip install tabulate