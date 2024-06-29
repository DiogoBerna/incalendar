import sqlite3

def setup_database():
    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone_number TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()

    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if 'phone_number' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN phone_number TEXT")
        conn.commit()

    conn.close()

if __name__ == "__main__":
    setup_database()
