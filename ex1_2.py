"""
Lurkers: How many users are there on the platform 
who have not interacted with posts or posted any 
content yet (but may have followed other users)?
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
    users = pd.read_sql_query("SELECT * FROM users;", conn)
    posts = pd.read_sql_query("SELECT * FROM posts;", conn)
    comments = pd.read_sql_query("SELECT * FROM comments;", conn)
    reactions = pd.read_sql_query("SELECT * FROM reactions;", conn)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()

lurkers = 0
for u in users['id']:
    if u not in posts['user_id'].values and \
       u not in comments['user_id'].values and \
       u not in reactions['user_id'].values:
        lurkers += 1


print(f'The number of lurkers in MiniSocial is: {lurkers}')
