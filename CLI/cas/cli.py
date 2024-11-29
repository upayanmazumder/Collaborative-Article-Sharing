import os
import json
import webbrowser
import sys
import requests
from flask import Flask, Blueprint, request, jsonify, redirect

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

    # Redirect user to the success page after successful auth
    return redirect("https://cas.upayan.dev/auth/connect/success")

@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200  # Prevent favicon requests from interfering

# Add article function to interact with the API
def add_article(article):
    """
    Adds a article to the user's database entry using the API.
    Ensures the user is logged in before proceeding.
    """
    session_details = load_session_details()
    if not session_details or "email" not in session_details or "token" not in session_details:
        print("Error: User is not logged in. Please log in first.")
        return

    api_url = "https://api.cas.upayan.dev/push"
    headers = {"Authorization": session_details["token"]}
    payload = {"article": article}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Article added successfully:", response.json())
        else:
            print("Failed to add article. Error:", response.json())
    except requests.RequestException as e:
        print("Error while communicating with the API:", e)

# Show help article
def show_help():
    help_article = """
    Usage:
        cas help                            Show this help article.
        cas auth                            Start authentication process.
        cas push <article-link>             Add an article.
    """
    print(help_article)

# Main function to handle CLI and web server logic
def main():
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "push":
        if len(sys.argv) < 3:
            print("Usage: cas push <article-link>")
        else:
            article = " ".join(sys.argv[2:])
            add_article(article)
    elif sys.argv[1] == "help":
        show_help()
    elif sys.argv[1] == "auth":
        url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
        webbrowser.open(url)
        print("Starting server on http://localhost:8000")
        app = Flask(__name__)
        app.register_blueprint(auth_bp)
        app.run(port=8000)
    else:
        show_help()

# Entry point for CLI commands
if __name__ == "__main__":
    main()
