import os
import json
import requests
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from modules.get_user import get_user_function
from modules.create_user import create_user_function
from modules.is_calendar_connected import is_calendar_connected
from modules.calendar.call_setup import generate_auth_url, create_event, list_event
from modules.create_meeting import create_meeting_function

load_dotenv()

env_vars = [
    "OPENAI_KEY"
]

for var_name in env_vars:
    value = os.environ.get(var_name)
    if value is None:
        value = os.getenv(var_name)
    globals()[var_name] = value

def message_function(request_data):
  message_type = request_data.get('MessageType')
  if 'text' not in message_type:
    return "Only text messages are supported at the moment."
  
  message_from = request_data.get('From')
  message_from = message_from.replace("whatsapp:", "")
  message_body = request_data.get('Body')

  openai_key = globals()["OPENAI_KEY"]

  user = create_user_function(request_data)

  print("============")
  print(user)
  print("============")

  user_data = json.loads(user)


  client = OpenAI(
    api_key=openai_key,
  )

  chat_completion = client.chat.completions.create(
  messages=[
     {
        "role": "system",
        "content": f"{system_instructions} The user's name is {user_data['name']}. Today's date is {datetime.now().strftime('%Y-%m-%d')}."
      },
      {
          "role": "user",
          "content": message_body,
      }
  ],
  model="gpt-4o",
  tools=tools,
  tool_choice="auto"
  )

  if chat_completion.choices[0].message.tool_calls:
    data = None
    for tool_call in chat_completion.choices[0].message.tool_calls:
      if tool_call.function.name == "get_events":
        data = get_events(json.loads(tool_call.function.arguments), message_from)
      elif tool_call.function.name == "create_new_event":
        data = create_new_event(json.loads(tool_call.function.arguments), message_from)
      elif tool_call.function.name == "record_meeting":
        data = record_meeting(json.loads(tool_call.function.arguments), message_from)

    chat_completion = client.chat.completions.create(
    messages=[
        {
          "role": "system",
          "content": f"{system_instructions} The user's name is {user_data['name']}. Today's date is {datetime.now().strftime('%Y-%m-%d')}."
        },
        {
            "role": "user",
            "content": message_body,
        }, 
        {
          "role": "system",
          "content": data,
        }
    ],
    model="gpt-4o"
    ) 
  response_message = chat_completion.choices[0].message.content
  return response_message


def get_events(arguments, phone_number):
    print("get", arguments)
    is_connected = is_calendar_connected(phone_number)

    if not is_connected:
        message = "Before getting events, please connect your calendar. Then, ask me to get events again: "
        url = generate_auth_url(phone_number)
        return f"{message} {url}"
    
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")

    events = list_event(phone_number, start_date, end_date)
    # Logic to get events within the date range
    return f"{events}"

def get_events_array(arguments, phone_number):
    print("get", arguments)
    is_connected = is_calendar_connected(phone_number)

    if not is_connected:
        message = "Before getting events, please connect your calendar. Then, ask me to get events again: "
        url = generate_auth_url(phone_number)
        return f"{message} {url}"
    
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")

    events = list_event(phone_number, start_date, end_date)
    # Logic to get events within the date range
    return events

def create_new_event(arguments, phone_number):
    is_connected = is_calendar_connected(phone_number)

    if not is_connected:
        message = "Before creating an event, please connect your calendar. Then, ask me to create an event again: "
        url = generate_auth_url(phone_number)
        return f"{message} {url}"
    
    date_time = arguments.get("date_time")
    duration = arguments.get("duration", 30)
    attendees = arguments.get("attendees", [])
    title = arguments.get("title", "New Event - by InCalendar")
    create_event(phone_number, date_time, duration, title, attendees)
    # Logic to create a new event
    return f"New event created on {date_time} for {duration} minutes with attendees {attendees}"

def record_meeting(arguments, phone_number):
    is_connected = is_calendar_connected(phone_number)

    if not is_connected:
        message = "Before creating an event, please connect your calendar. Then, ask me to create an event again: "
        url = generate_auth_url(phone_number)
        return f"{message} {url}"
    
    print("record", arguments)
    if arguments.get("event_id"):
        meeting_url = arguments.get("meeting_url")
    else:
        events = get_events_array(arguments, phone_number)
        first_event = events[0] if events else None
        meeting_url = first_event.get("hangoutLink") if first_event else None

    json_meeting = {
        "meeting_url": meeting_url,
        "bot_name": "InCalendar Bot",
        "join_at": datetime.now().isoformat(),
        "automatic_leave": {"everyone_left_timeout": 5}
    }
    recall_api_key = os.getenv("RECALL_API_KEY")
    
    request = requests.post(
        "https://api.recall.ai/api/v1/bot/",
        json=json_meeting, 
        headers={"Authorization": f"Token {recall_api_key}"}
    )
    recall_data = request.json()
    print(recall_data)
    recall_id = recall_data.get("id")
    print("recall_id", recall_id)

    user = get_user_function(phone_number)
    user_data = json.loads(user)
    user_id = user_data.get("id")
    # recall_id = "1234"
    arguments = {
        "BotId": recall_id,
        "UserId": user_id
    }
    result = create_meeting_function(arguments)
    print(result)
    print("added to db")
    # Logic to record meeting details
    return f"System successfully scheduled recording for the event"

def find_event(arguments, phone_number):
    is_connected = is_calendar_connected(phone_number)

    if not is_connected:
        message = "Before finding an event, please connect your calendar. Then, ask me to find an event again: "
        url = generate_auth_url(phone_number)
        return f"{message} {url}"
    
    search_start_date = arguments.get("search_start_date")
    search_end_date = arguments.get("search_end_date")
    # Logic to find event ID
    return {
       "id": "3bqqehufoqk3htb3vicrhh5ct0",
       "summary": "Hackathon",
       "start": "2024-06-29T18:00:00-07:00",
       "end": "2024-06-29T19:00:00-07:00"
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_events",
            "description": "Get events within a date range",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                },
                "required": ["start_date", "end_date"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_new_event",
            "description": "Create a new event",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_time": {"type": "string", "description": "Date and time of the event"},
                    "duration": {"type": "integer", "description": "Duration of the event in minutes"},
                    "attendees": {"type": "array", "items": {"type": "string"}, "description": "List of attendee email addresses"},
                    "title": {"type": "string", "description": "Title of the event"}
                },
                "required": ["date_time", "title"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_meeting",
            "description": "Record meeting details",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "ID of the event to record"},
                    "start_date": {"type": "string", "description": "If no ID is provided, search for events starting from this date"},
                    "end_date": {"type": "string", "description": "If no ID is provided, search for events ending on this date"}
                }
            },
        }
    }
]

system_instructions = """
You are the InCalendar helpful calendar assistant available via Whatsapp. Do not help with unrelated things.
1. You can help with scheduling (the user will often forward an email address they receive and wish to schedule a meeting for)
2. You can help with briefing the user on their schedule
3. You can help record meetings by inviting the InCalendar Meeting Bot 
4. Always use plain text for responses, and never markdown formatting or HTML
"""