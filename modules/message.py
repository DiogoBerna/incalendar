import json

from modules.create_user import create_user_function

def message_function(request_data):
  message_from = request_data.get('From')
  message_body = request_data.get('Body')

  user = create_user_function(request_data)

  print("============")
  print(user)
  print("============")

  user_data = json.loads(user)


  # OPENAI CODE GOES HERE!!!


  message = f"Hello, {user_data['name']}. How can I help you today?"
  return message
