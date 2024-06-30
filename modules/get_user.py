import json
import sqlite3

def get_user_function(phone_number):
    try:
        if phone_number.startswith(" "):
            phone_number = f"+{phone_number.strip()}"

        conn = sqlite3.connect('incalendar.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
        user = c.fetchone()

        if user:
            column_names = [description[0] for description in c.description]
            user_dict = dict(zip(column_names, user))
            return json.dumps(user_dict)
        else:
            return json.dumps({'error': 'User not found.'})
    except sqlite3.Error as e:
        return json.dumps({'error': str(e)})
    finally:
        if conn:
            conn.close()
