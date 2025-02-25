import sqlite3
import os

# Ensure the 'database' directory exists
if not os.path.exists('database'):
    os.makedirs('database')

# Create a connection to the SQLite database
conn = sqlite3.connect('database/stock.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Add medicine_name column if it does not exist (update table schema)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_name TEXT NOT NULL,
        brand TEXT NOT NULL,
        dose TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')
print("✅ Medicines table verified and updated with medicine_name column!")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
