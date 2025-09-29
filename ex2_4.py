"""
Connections: Identify the top 3 user pairs who engage 
with each other's content the most. Define and describe 
your metric for engagement.
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
    connections_query = """
SELECT
	u1.username,
	u2.username,
	COUNT(*) AS engagement
FROM posts p
JOIN (
	SELECT
		user_id,
		post_id
	FROM comments
	UNION ALL
	SELECT
		user_id,
		post_id
	FROM reactions
) AS e ON p.id = e.post_id AND p.user_id != e.user_id
JOIN users u1 ON u1.id = p.user_id
JOIN users u2 ON u2.id = e.user_id
GROUP BY MIN(p.user_id, e.user_id), MAX(p.user_id, e.user_id)
ORDER BY engagement DESC
LIMIT 3;
"""
    connections = pd.read_sql_query(connections_query, conn)
    print(connections)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()


