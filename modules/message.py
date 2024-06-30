import os
import json

from dotenv import load_dotenv
from modules.create_user import create_user_function
# from modules.calendar.functions import list_event
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
  message_from = request_data.get('From')
  message_body = request_data.get('Body')

  openai_key = globals()["OPENAI_KEY"]

  user = create_user_function(request_data)
  user_data = json.loads(user)

  print("============")
  print(user)
  print("============")



  # OPENAI CODE GOES HERE!!!
  # message = get_calendar_service()
  # message = generate_auth_url(user_data['phone_number'])
  create_event(user_data['phone_number'])


  # message = f"Hello, {user_data['name']}. How can I help you today?"
  message = "Event created successfully!"
  return message
