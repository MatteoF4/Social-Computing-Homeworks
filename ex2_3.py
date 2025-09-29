"""
Content Lifecycle: What is the average time between the 
publishing of a post and the first engagement it receives? 
What is the average time between the publishing of a post 
and the last engagement it receives?
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
    first_comment_query = """
SELECT
	AVG(first_comment_time) AS avg_first
FROM (
	SELECT
		(julianday(MIN(c.created_at)) - julianday(p.created_at)) AS first_comment_time
	FROM posts p
	JOIN comments c ON p.id = c.post_id
	GROUP BY p.id
)
"""
    last_comment_query = """
SELECT
	AVG(last_comment_time) AS avg_last
FROM (
	SELECT
		(julianday(MAX(c.created_at)) - julianday(p.created_at)) AS last_comment_time
	FROM posts p
	JOIN comments c ON p.id = c.post_id
	GROUP BY p.id
)
"""
    first_comment = pd.read_sql_query(first_comment_query, conn)
    last_comment = pd.read_sql_query(last_comment_query, conn)

    print(f"Average time for a post to receive its:\n- First comment: \
          {first_comment['avg_first'].iloc[0]} days\n- Last comment: \
            {last_comment['avg_last'].iloc[0]} days")

except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()
