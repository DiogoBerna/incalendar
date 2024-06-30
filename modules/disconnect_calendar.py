import json
import sqlite3

def disconnect_calendar_function(request_data):
  phone_number = request_data.get('phone_number')
  try:

    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()
    
    print(phone_number)
    c.execute("UPDATE users SET calendar_token = ?, calendar_token_refresh = ? WHERE phone_number = ?", ("", "", phone_number))
    conn.commit()
    conn.close()

    return json.dumps({'message': 'Calendar disconnected successfully'})
  except sqlite3.Error as e:
    return json.dumps({'error': str(e)})
  finally:
    if conn:
      conn.close()
