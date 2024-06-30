import json
import sqlite3

def create_meeting_function(request_data):
    try:
        bot_id = request_data.get('BotId')
        if not bot_id:
            return json.dumps({'error': 'Bot ID is required.'})
        
        user_id = request_data.get('UserId')
        bot_status = request_data.get('BotStatus', "Pending")
        transcription = request_data.get('Transcription', "")
        transcription_status = request_data.get('TranscriptionStatus', "Not Started")
        
        conn = sqlite3.connect('incalendar.db')
        c = conn.cursor()
        
        # Insert new meeting
        c.execute('''
            INSERT INTO meetings (bot_id, user_id, bot_status, transcription, transcription_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id, user_id, bot_status, transcription, transcription_status))
        conn.commit()
        
        meeting_id = c.lastrowid
        return json.dumps({'id': meeting_id, 'bot_id': bot_id, 'user_id': user_id, 'bot_status': bot_status, 'transcription': transcription, 'transcription_status': transcription_status})
    except sqlite3.Error as e:
        return json.dumps({'error': str(e)})
    finally:
        if conn:
            conn.close()