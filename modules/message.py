import json

from modules.create_user import create_user_function

def message_function(request_data):
  print("============")
  print("============")
  print("============")
  print(request_data)
  print("============")
  print("============")
  print("============")

  message_from = request_data.get('From')
  message_body = request_data.get('Body')

  create_user_function(request_data)

  return "Message sent successfully."