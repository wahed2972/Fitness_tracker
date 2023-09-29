import sqlite3

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect('fitness.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define a table for user information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Define a table for workout information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        workout_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        workout_name TEXT NOT NULL,
        workout_description TEXT,
        workout_date DATE,
        workout_time TIME,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()
