"""
Virality: Identify the 3 most viral posts in the history 
of the platform. Select and justify a specific metric or 
requirements for a post to be considered viral. 
"""
# To normalize virality index, only for style purposes
# since julianday if left as absolute number gets way too big
norm = 100000

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
    virality_query = f"""
SELECT
	p.id AS "post's id",
	({norm}*COUNT(c.id) / (AVG(julianday(c.created_at)))) AS virality
FROM posts p
JOIN comments c on p.id = c.post_id
GROUP BY p.id
ORDER BY virality DESC
LIMIT 3;
"""
    virality = pd.read_sql_query(virality_query, conn)
    print(virality)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()
