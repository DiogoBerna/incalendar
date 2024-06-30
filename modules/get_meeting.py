import json
import sqlite3

def get_meeting_function(bot_id):
    try:
        conn = sqlite3.connect('incalendar.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM meetings WHERE bot_id = ?", (bot_id,))
        meeting = c.fetchone()

        if meeting:
            column_names = [description[0] for description in c.description]
            meeting_dict = dict(zip(column_names, meeting))
            return json.dumps(meeting_dict)
        else:
            return json.dumps({'error': 'Meeting not found.'})
    except sqlite3.Error as e:
        return json.dumps({'error': str(e)})
    finally:
        if conn:
            conn.close()