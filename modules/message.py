import os
import json

from dotenv import load_dotenv
from modules.create_user import create_user_function

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

  print("============")
  print(user)
  print("============")

  user_data = json.loads(user)


  # OPENAI CODE GOES HERE!!!


  message = f"Hello, {user_data['name']}. How can I help you today?"
  return message