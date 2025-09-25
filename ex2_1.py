"""
Growth: This year, we are renting 16 servers to run our 
social media platform. They are soon at 100% capacity, 
so we need to rent more servers. We would like to rent 
enough to last for 3 more years without upgrades, plus 
20% capacity for redundancy. We need an estimate of how 
many servers we need to start renting based on past 
growth trends.
Plot the trend on a graph using Python and include it 
below. (Note that the dataset may not end in the current 
year, please assume that the last data marks today's date)
"""
initial_servers = 16
future_years = 3
redundancy = 0.2

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import numpy as np

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
    yearly_growth_query = """
SELECT 
	STRFTIME('%Y', created_at) AS year,
	SUM(COUNT(*)) OVER (ORDER BY STRFTIME('%Y', created_at)) AS growth
FROM (
    SELECT created_at FROM comments
    UNION ALL
    SELECT created_at FROM posts
    UNION ALL
    SELECT created_at FROM users
)
GROUP BY year;
"""
    yearly_growth = pd.read_sql_query(yearly_growth_query, conn)
except Exception as e:
    print(f"Error while loading data: '{e}'")
finally:
    if conn:
        conn.close()

# Calculate future growth
server_capacity = yearly_growth['growth'].iloc[-1] /initial_servers

x = list([int(e) for e in yearly_growth['year']])
y = list([int(e) for e in yearly_growth['growth']])

m, q = np.polyfit(x, y, 1)

trend_x = np.array([x[0]+i for i in range(len(x)+future_years)])
trend_y = m*trend_x+q

new_x = [x[-1], trend_x[-1]]
new_y = [y[-1], trend_y[-1]]

# Calculate the needed servers
future_servers = trend_y[-1]/server_capacity
future_servers += (future_servers-initial_servers)*redundancy
future_servers = int(future_servers)
print(f'In the next {future_years} years, MiniSocial will need to buy {future_servers-initial_servers} new servers.')

# Plot the trend
plt.plot(trend_x, trend_y, color='red', label='Growth Trend')
plt.plot(x, y, color='blue', label='Past Growth')
plt.plot(new_x, new_y, color='cyan', label='Estimated Future Growth')

plt.gcf().canvas.manager.set_window_title("MiniSocial's yearly growth")
plt.title("MiniSocial's growth during the years")
plt.xlabel('Year')
plt.ylabel('Growth')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

plt.show()
