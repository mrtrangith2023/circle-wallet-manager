import sqlite3

conn = sqlite3.connect("circle.db")

cursor = conn.cursor()

cursor.execute("""
UPDATE users
SET role='ADMIN'
WHERE username='admin'
""")

cursor.execute("""
UPDATE users
SET role='USER'
WHERE username='user1'
""")

conn.commit()

conn.close()

print("Done")