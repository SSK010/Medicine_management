import sqlite3
import os
import bcrypt

# Ensure database directory exists
if not os.path.exists('database'):
    os.makedirs('database')

# ✅ Connect to the SQLite database
conn = sqlite3.connect('database/stock.db')
cursor = conn.cursor()

# ✅ Create/Update Vitals Table (Add O₂ Column)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vitals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        date TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        bp_systolic INTEGER DEFAULT NULL,
        bp_diastolic INTEGER DEFAULT NULL,
        pulse INTEGER DEFAULT NULL,
        spo2 INTEGER DEFAULT NULL,
        o2 INTEGER DEFAULT NULL,  -- Added O₂ column
        temp REAL DEFAULT NULL,
        smbg REAL DEFAULT NULL
    )
''')
print("✅ Vitals table verified & updated with O₂ column!")

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

# Insert default users if not already present
default_users = [
    ('admin', 'admin123', 'Admin'),
    ('doctor', 'doctor123', 'Doctor'),
    ('nurse', 'nurse123', 'Nurse'),
    ('guest', 'guest123', 'Guest')
]
for username, password, role in default_users:
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:  # Only insert if user does not exist
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password.decode('utf-8'), role))
print("✅ Default users added or already exist!")

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

# Create Feeding Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feeding (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        feed_type TEXT NOT NULL,
        feed_quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Feeding table created successfully!")

# Create Medication Advice Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medication_advice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        medicine_name TEXT NOT NULL,  -- Medicine Name for advice (e.g., PCT)
        brand TEXT NOT NULL,       -- Medicine Brand (e.g., Neomol, Breomol)
        dose TEXT NOT NULL,           -- Medicine Dose (e.g., 500mg)
        quantity INTEGER NOT NULL,    -- Quantity of medicine
        from_date TEXT NOT NULL,      -- Date advice starts
        to_date TEXT                 -- Optional date advice ends
    )
''')
print("✅ Medication advice table created successfully!")

# ✅ Create Administered Medicines Table
# ✅ Drop old administered_medicines table if it exists (prevents structure issues)
cursor.execute('DROP TABLE IF EXISTS administered_medicines')

# ✅ Recreate Administered Medicines Table
cursor.execute('''
    CREATE TABLE administered_medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
    )
''')
print("✅ Administered Medicines table recreated successfully!")

# Create Withhold Medicine Table
# Ensure the withhold_medicine table exists
cursor.execute('''
        CREATE TABLE IF NOT EXISTS withhold_medicine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            medicine_name TEXT NOT NULL,  -- Medicine Name for withhold advice (e.g., PCT)
            dose TEXT NOT NULL,           -- Medicine Dose (e.g., 500mg)
            brand TEXT NOT NULL,          -- Medicine Brand (e.g., Neomol, Breomol)
            quantity INTEGER NOT NULL,    -- Quantity to withhold
            from_date TEXT NOT NULL,      -- Date withhold starts
            to_date TEXT                  -- Optional date withhold ends
        )
    ''')
conn.commit()
print("✅ Withhold medicine table created successfully!")

# ✅ Save changes **before** closing the connection
conn.commit()
conn.close()

print("✅ Database update completed successfully!")
