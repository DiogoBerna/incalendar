import json
import sqlite3

def create_user_function(request_data):
    try:
        phone_number = request_data.get('From')
        if not phone_number:
            return json.dumps({'error': 'Phone Number is required.'})
        
        name = request_data.get('ProfileName', "Unknown")
        conn = sqlite3.connect('incalendar.db')
        c = conn.cursor()
        
        # Corrected tuple format for the query
        c.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
        existing_user = c.fetchone()
        
        if existing_user:
            # Corrected tuple format for the update statement
            c.execute("UPDATE users SET name = ? WHERE phone_number = ?", (name, phone_number))
            conn.commit()
            return json.dumps({'message': 'User info updated', 'name': name, 'phone_number': phone_number})
        else:
            # Corrected tuple format for the insert statement
            c.execute("INSERT INTO users (name, phone_number) VALUES (?, ?)", (name, phone_number))
            conn.commit()
            
            user_id = c.lastrowid
            return json.dumps({'id': user_id, 'name': name, 'phone_number': phone_number})
    except sqlite3.Error as e:
        return json.dumps({'error': str(e)})
    finally:
        if conn:
            conn.close()
