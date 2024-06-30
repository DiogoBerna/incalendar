import json
import sqlite3

def is_calendar_connected(phone_number):
    is_connected = False
    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
    user = c.fetchone()

    print(user)

    if user and user[3] and user[4]:
      is_connected = True

    conn.close()
    return is_connected
