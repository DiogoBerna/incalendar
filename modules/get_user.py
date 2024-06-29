import json
import sqlite3

def get_user_function(phone_number):
    try:
        conn = sqlite3.connect('incalendar.db')
        c = conn.cursor()
        
        # Query the user by ID
        c.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
        user = c.fetchone()

        if user:
            return json.dumps({'id': user[0], 'phone_number': user[3]})
        else:
            return json.dumps({'error': 'User not found.'})
    except sqlite3.Error as e:
        return json.dumps({'error': str(e)})
    finally:
        if conn:
            conn.close()
