import os
import json

from flask_cors import CORS
from flask_session import Session
from flask import Flask, jsonify, request, got_request_exception

# modules
from modules.status import get_status
from modules.message import message_function
from modules.get_user import get_user_function
from modules.create_user import create_user_function
from modules.calendar.call_setup import get_calendar_service
from modules.disconnect_calendar import disconnect_calendar_function
from modules.get_meeting import get_meeting_function

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "session_data"
app.config["SESSION_FILE_THRESHOLD"] = 100
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
Session(app)

app.add_url_rule("/status", view_func=get_status, methods=["GET"])

@app.route("/get_user", methods=["GET"])
def start_get_user():
  phone_number = request.args.get('phone_number')
  if not phone_number:
    return json.dumps({'error': 'Phone Number is required.'})
  
  result = get_user_function(phone_number)
  return result

@app.route("/disconnect_calendar", methods=["POST"])
def start_disconnect_calendar():
  request_data = request.get_json()
  result = disconnect_calendar_function(request_data)
  return result

@app.route("/create_user", methods=["POST"])
def start_create_user():
  request_data = request.get_json()
  result = create_user_function(request_data)
  return result

@app.route("/message", methods=["POST"])
def start_message():
  request_data = request.form
  result = message_function(request_data)
  return result, 200, {'Content-Type': 'text/plain'}

@app.route("/authorize", methods=["GET"])
def start_authorize():
  code = request.args.get('code')
  state = request.args.get('state')
  get_calendar_service(state, code)
  return "Linked calendar with access. You can close this tab and return to the InCalendar conversation on Whatsapp", 200

@app.route("/call-bot", methods=["POST"])
def call_bot_event():
  print(request.data)
  data = request.get_json()
  bot_id = data.get("data", {}).get("bot_id")
  result = get_meeting_function(bot_id)
  return result

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(debug=True, host="0.0.0.0", port=port)
