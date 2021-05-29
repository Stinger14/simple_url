import sqlite3

# create connection to db, creates db if doesn't exist
conn = sqlite3.connect('database.db')

# this will delete all of the existing data whenever 
# the schema file executes.
with open('schema.sql') as f:
    conn.executescript(f.read())

# commit changes and close connection.
conn.commit()
conn.close()
