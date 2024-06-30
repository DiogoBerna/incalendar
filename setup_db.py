import sqlite3

def setup_database():
    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone_number TEXT NOT NULL UNIQUE,
            calendar_token TEXT,
            calendar_token_refresh TEXT
        )
    ''')
    conn.commit()

    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if 'calendar_token' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN calendar_token TEXT")
        conn.commit()
    if 'calendar_token_refresh' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN calendar_token_refresh TEXT")
        conn.commit()

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()

    # New table creation
    c.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY,
            bot_id TEXT NOT NULL,
            user_id INTEGER,
            bot_status TEXT,
            transcription TEXT,
            transcription_status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()

    conn.close()

if __name__ == "__main__":
    setup_database()
