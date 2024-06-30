import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from modules.create_user import create_user_function
from modules.calendar.call_setup import get_calendar_service, generate_auth_url, create_event

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
  if request_data.get('MessageType') is not 'text':
    return "Only text messages are supported at the moment."
  
  message_from = request_data.get('From')
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
  # Check for tool calls
  if chat_completion.choices[0].message.tool_calls:
    data = None
    for tool_call in chat_completion.choices[0].message.tool_calls:
      if tool_call.function.name == "get_events":
        data = get_events(json.loads(tool_call.function.arguments))
      elif tool_call.function.name == "create_new_event":
        data = create_new_event(json.loads(tool_call.function.arguments))
      elif tool_call.function.name == "record_meeting":
        data = record_meeting(json.loads(tool_call.function.arguments))

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


def get_events(arguments):
    print("get", arguments)
    start_date = arguments.get("start_date")
    end_date = arguments.get("end_date")
    # Logic to get events within the date range
    return f"Events from {start_date} to {end_date}"

def create_new_event(arguments):
    print("create", arguments)
    # create_event(user_data['phone_number'])
    date_time = arguments.get("date_time")
    duration = arguments.get("duration", 30)  # Default to 30 minutes if not specified
    attendees = arguments.get("attendees", [])
    # Logic to create a new event
    return f"New event created on {date_time} for {duration} minutes with attendees {attendees}"

def record_meeting(arguments):
    print("record", arguments)
    if arguments.get("event_id"):
        event_id = arguments.get("event_id")
    else:
        event = find_event(arguments)
        
       
    # Logic to record meeting details
    return f"System successfully scheduled recording for the event"

def find_event(arguments):
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
                    "search_start_date": {"type": "string", "description": "If no ID is provided, search for events starting from this date"},
                    "search_end_date": {"type": "string", "description": "If no ID is provided, search for events ending on this date"}
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
"""