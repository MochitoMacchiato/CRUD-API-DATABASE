import sqlite3

# Established a connection and cursor
conn = sqlite3.connect("tasks.db")
cur = conn.cursor()

# Sample tasks to be inserted (if table is empty)
tasks = [
    ("Wake up!", 1),
    ("Fix bed", 0),
    ("Eat cereal", 0)
]

cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id integer PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")

cur.execute("SELECT COUNT(*) FROM tasks")
result = cur.fetchone()[0]
if result == 0:
    cur.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",    
        tasks
    )

conn.commit()
conn.close()