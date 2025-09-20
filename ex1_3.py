"""
Influencers: In the history of the platform, who 
are the 5 users with the most engagement on their 
posts? 
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
    # Comments = 2, Reactions = 1
    influencers_query = """
SELECT
    users.username AS Influencer,
    (
    COUNT(DISTINCT comments.id)*2 + 
    COUNT(DISTINCT reactions.id)
    ) AS Engagement
FROM posts
LEFT JOIN comments ON comments.post_id = posts.id
LEFT JOIN reactions ON reactions.post_id = posts.id
JOIN users ON users.id = posts.user_id
GROUP BY users.id
ORDER BY engagement DESC
LIMIT 5;
"""
    influencers = pd.read_sql_query(influencers_query, conn)
    print(influencers)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()
