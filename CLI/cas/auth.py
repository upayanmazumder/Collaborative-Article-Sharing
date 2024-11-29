import os
import json
from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)
session_file = "session.json"

def load_session_details():
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            return json.load(f)
    return {}

def save_session_details(details):
    with open(session_file, "w") as f:
        json.dump(details, f)

@auth_bp.route("/")
def handle_auth_response():
    email = request.args.get("email", "")
    token = request.args.get("token", "")

    # Only update session details if email and token are present
    if email and token:
        session_details = {"email": email, "token": token}
        save_session_details(session_details)
        print("Session details saved:", session_details)
    else:
        print("Invalid or empty session details, skipping update.")

    return jsonify({"status": "ok", "session_details": load_session_details()})


@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200  # Prevent favicon requests from interfering
