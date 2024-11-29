import os
import json
import webbrowser
import sys
import requests
from flask import Flask, Blueprint, request, jsonify

# Define the auth blueprint and session management functions
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

# Add message function to interact with the API
def add_message(message):
    """
    Adds a message to the user's database entry using the API.
    Ensures the user is logged in before proceeding.
    """
    session_details = load_session_details()
    if not session_details or "email" not in session_details or "token" not in session_details:
        print("Error: User is not logged in. Please log in first.")
        return

    api_url = "https://api.cas.upayan.dev/add-message"
    headers = {"Authorization": session_details["token"]}
    payload = {"message": message}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Message added successfully:", response.json())
        else:
            print("Failed to add message. Error:", response.json())
    except requests.RequestException as e:
        print("Error while communicating with the API:", e)

# Main function to handle CLI and web server logic
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "add-message":
        if len(sys.argv) < 3:
            print("Usage: cli.py add-message <your-message>")
        else:
            message = " ".join(sys.argv[2:])
            add_message(message)
    else:
        url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
        webbrowser.open(url)
        print("Starting server on http://localhost:8000")
        app = Flask(__name__)
        app.register_blueprint(auth_bp)
        app.run(port=8000)

# Entry point for CLI commands
if __name__ == "__main__":
    main()
