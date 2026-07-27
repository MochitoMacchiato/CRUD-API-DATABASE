import sqlite3

DATABASE = "tasks.db"

# Established a connection and cursor
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
            id integer PRIMARY KEY,
            title TEXT,
            done BOOLEAN
        )
    """)

    cur.execute("SELECT COUNT(*) FROM tasks")
    result = cur.fetchone()[0]

    if result == 0:
        tasks = [
            ("Wake up!", 1),
            ("Fix bed", 0),
            ("Eat cereal", 0)
        ]
        cur.executemany(
            "INSERT INTO tasks (title, done) VALUES (?,?)",
            tasks
        )
    conn.commit()
    conn.close()

init_db()

