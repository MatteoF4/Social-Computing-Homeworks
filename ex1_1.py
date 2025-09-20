"""
Reading the dataset: Load the database and for each table, 
print and inspect the available columns and the number of 
rows. For each 
table, describe all columns (name, purpose, type, example 
of contents). 
"""

import pandas as pd
import sqlite3

# Optional for clearing the terminal at each run
import os
os.system('clear')

# Connect to the database
DB_FILE = "minisocial_database.sqlite"
try:
    conn = sqlite3.connect(DB_FILE)
except Exception as e:
    print(f"Couldn't connect to the Database: '{e}'")

try:
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    for t in tables['name']:
        # Get columns' names and other info
        columns = pd.read_sql_query(f"PRAGMA table_info({t})", conn)
        # I interpeted "inspect" as this, if it meant to print the contents then
        # I would have used something like "SELECT * FROM {t} LIMIT 5"

        # Count the number of rows
        rows_count = pd.read_sql_query(f"SELECT COUNT(*) AS count FROM {t};", conn)

        # Print results
        print('*'*32)
        print(f"Table '{t}' columns' info:\n")
        print(columns)
        print(f'\nThe table has {rows_count['count'].iloc[0]} rows.\n')

except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()
