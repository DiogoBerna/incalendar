import googleapiclient
from datetime import datetime, timedelta
from modules.calendar.call_setup import get_calendar_service


def main():
    print("-----------------------")
    print("-----------------------")
    print("GOOGLE CALENDAR AUTOMATION")
    print("1. List your calendar")
    print("2. Create an event")
    print("3. List your event")
    print("4. Update an event")
    print("5. Delete an event")
    print(("-----------------------"))
    print(("-----------------------"))


def list_cal():

    print("List all calendar")
    service = get_calendar_service()

    print('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        id = calendar['id']
        primary = "Primary" if calendar.get('primary') else ""
        print("%s\t%s\t%s" % (summary, id, primary))

def create_event():

    print("Create an event")
    a = input("Describe the event: ")
    service = get_calendar_service()

    date = datetime.now().date()
    today = datetime(date.year, date.month, date.day, 10) + timedelta(days=0)
    start = today.isoformat()
    end = (today + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": 'AAKASH --- CALENDAR AUTOMATION',
                                               "description": a,
                                               "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                                               "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                                           }
                                           ).execute()

    print("Calendar Automation has created an event")
    print("Id: ", event_result['id'])
    print("Summary: ", event_result['summary'])
    print("Starts At: ", event_result['start']['dateTime'])
    print("Ends At: ", event_result['end']['dateTime'])


def list_event():
    import datetime

    print("List 10 upcoming events")
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting List of 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def update_event():

    print("Update an event")
    service = get_calendar_service()
    al = input("Enter Calender ID: ")
    eid = input("Enter Event ID: ")
    a = input("Describe the new event: ")

    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 9) + timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=2)).isoformat()

    event_result = service.events().update(
        calendarId=al,
        eventId=eid,
        body={
        "summary": 'AAKASH --- CALENDAR AUTOMATION',
        "description": a,
        "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
        "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
        },
         ).execute()


    print("Updated Event: ", eid)
    print("Id: ", event_result['id'])
    print("Summary: ", event_result['summary'])
    print("Starts At: ", event_result['start']['dateTime'])
    print("Ends At: ", event_result['end']['dateTime'])

def delete_event():

    print("Delete an event")
    service = get_calendar_service()
    cal = input("Enter Calender ID: ")
    eid = input("Enter Event ID: ")
    try:
        service.events().delete(
            calendarId=cal,
            eventId=eid,
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")


while True:
    main()
    c = input("Enter your choice: ")
    if c == '1':
        list_cal()
    elif c == '2':
        create_event()
    elif c == '3':
        list_event()
    elif c == '4':
        update_event()
    elif c == '5':
        delete_event()
    else:
        break