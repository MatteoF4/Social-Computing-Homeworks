"""
Spammers: Identify users who have shared the same 
text in posts or comments at least 3 times over 
and over again (in all their history, not just 
the last 3 contributions).
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
    spammers_query = """
SELECT DISTINCT
    user_id AS spammer_id,
    users.username AS spammer_username
FROM (
    SELECT
        user_id,
        content
    FROM comments
    UNION ALL
    SELECT
        user_id,
        content
    FROM posts
)
JOIN users ON user_id = users.id
GROUP BY user_id, content
HAVING COUNT(*) >= 3;
"""
    spammers = pd.read_sql_query(spammers_query, conn)
    print(spammers)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()
