import os.path
import sqlite3
from datetime import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'

def generate_auth_url(phone_number):
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='https://adb4-76-132-138-253.ngrok-free.app/authorize')
    auth_url, _ = flow.authorization_url(prompt='consent', state=phone_number)
    return auth_url

def save_tokens_to_db(phone_number, token, refresh_token):
    if phone_number.startswith(" "):
        phone_number = f"+{phone_number.strip()}"

    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()
    c.execute("UPDATE users SET calendar_token = ?, calendar_token_refresh = ? WHERE phone_number = ?", (token, refresh_token, phone_number))
    conn.commit()
    conn.close()

def get_tokens_from_db(phone_number):
    if phone_number.startswith(" "):
        phone_number = f"+{phone_number.strip()}"

    conn = sqlite3.connect('incalendar.db')
    c = conn.cursor()
    c.execute("SELECT calendar_token, calendar_token_refresh FROM users WHERE phone_number = ?", (phone_number,))
    result = c.fetchone()
    conn.close()
    return result

def get_calendar_service(phone_number, auth_code=None):
    tokens = get_tokens_from_db(phone_number)
    if tokens:
        token, refresh_token = tokens
    else:
        token, refresh_token = None, None

    cred = None

    if token and refresh_token:
        creds = Credentials(token, refresh_token=refresh_token, token_uri='https://oauth2.googleapis.com/token',
                            client_id='<YOUR_CLIENT_ID>', client_secret='<YOUR_CLIENT_SECRET>')
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_tokens_to_db(phone_number, creds.token, creds.refresh_token)
        cred = creds
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri='https://adb4-76-132-138-253.ngrok-free.app/authorize')
        flow.fetch_token(code=auth_code)
        cred = flow.credentials
        save_tokens_to_db(phone_number, cred.token, cred.refresh_token)

    service = build('calendar', 'v3', credentials=cred)
    print("Calendar service created successfully")
    return service

def create_event(phone_number, date_time, duration, title, attendees=[]):
    service = get_calendar_service(phone_number)
    print("Create an event")
    print("Title: ", title)
    print("Date Time: ", date_time)
    print("Duration: ", duration)
    print("Attendees: ", attendees)
    a = "Event created by InCalendar Automation"

    start = date_time
    end = (datetime.fromisoformat(date_time) + timedelta(minutes=duration)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": title,
                                               "description": "Event created by InCalendar Automation",
                                               "start": {"dateTime": start, "timeZone": 'America/Los_Angeles'},
                                               "end": {"dateTime": end, "timeZone": 'America/Los_Angeles'},
                                               "attendees": [{"email": attendee} for attendee in attendees],
                                               "conferenceData": {
                                                   "createRequest": {
                                                       "requestId": "12345",
                                                       "conferenceSolutionKey": {
                                                           "type": "hangoutsMeet"
                                                       }
                                                   }
                                               }
                                           },
                                           conferenceDataVersion=1
                                           ).execute()

    print("Calendar Automation has created an event")
    print("Id: ", event_result['id'])
    print("Summary: ", event_result['summary'])
    print("Starts At: ", event_result['start']['dateTime'])
    print("Ends At: ", event_result['end']['dateTime'])
    print("Google Meet Link: ", event_result['hangoutLink'])

def list_event(phone_number, start_date, end_date):
    print("List 10 upcoming events", phone_number)
    service = get_calendar_service(phone_number)

    now = datetime.utcnow().isoformat() + 'Z'
    print('Getting List of 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return "No upcoming events found."
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        return events