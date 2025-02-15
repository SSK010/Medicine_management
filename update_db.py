import sqlite3
import os
import bcrypt

# Ensure database directory exists
if not os.path.exists('database'):
    os.makedirs('database')

# Connect to the SQLite database
conn = sqlite3.connect('database/stock.db')
cursor = conn.cursor()

# ✅ Create Vitals table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        bp_systolic INTEGER,
        bp_diastolic INTEGER,
        pulse INTEGER,
        spo2 INTEGER,
        temp REAL,
        smbg REAL,
        date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Vitals table created successfully!")

# ✅ Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
print("✅ Users table created successfully!")

# Insert default users
default_users = [
    ('admin', 'admin123', 'Admin'),
    ('doctor', 'doctor123', 'Doctor'),
    ('nurse', 'nurse123', 'Nurse'),
    ('guest', 'guest123', 'Guest')
]
for username, password, role in default_users:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                   (username, hashed_password.decode('utf-8'), role))
print("✅ Default users added!")

# ✅ Create Intake & Output table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS intake_output (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        water_intake INTEGER DEFAULT 0,
        urine_output INTEGER DEFAULT 0,
        diaper_change TEXT DEFAULT 'No'
    )
''')
print("✅ Intake & Output table created successfully!")

# ✅ Create Patient Checklist table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        bathing TEXT DEFAULT 'No',
        position_change TEXT DEFAULT 'No',
        feeding TEXT DEFAULT 'No',
        medication_given TEXT DEFAULT 'No',
        dressing_change TEXT DEFAULT 'No',
        restrainer_tied TEXT DEFAULT 'No',
        restrainer_removed TEXT DEFAULT 'No'
    )
''')
print("✅ Patient Checklist table created successfully!")

# ✅ Create Patient Notes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        patient_name TEXT NOT NULL,
        note TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Patient Notes table created successfully!")

# ✅ Create Patient Names table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_names (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')
print("✅ Patient Names table created successfully!")

# Commit and close connection
conn.commit()
conn.close()
print("✅ Database update completed successfully!")
