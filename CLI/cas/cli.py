import webbrowser
from flask import Flask
from auth import auth_bp, load_session_details
import requests
import sys

app = Flask(__name__)

# Register the auth blueprint
app.register_blueprint(auth_bp)


def add_message(message):
    """
    Adds a message to the user's database entry using the API.
    Ensures the user is logged in before proceeding.
    """
    session_details = load_session_details()
    if not session_details or "email" not in session_details or "token" not in session_details:
        print("Error: User is not logged in. Please log in first.")
        return

    api_url = "https://api.cas.upayan.dev/add-message"  # Replace with your API's URL
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


if __name__ == "__main__":
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
        app.run(port=8000)
