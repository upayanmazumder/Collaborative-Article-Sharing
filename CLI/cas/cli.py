import argparse
import json
import os
import requests
import webbrowser

# Next.js Site URL
SITE_URL = "https://cas.upayan.dev"

def get_firebase_cli_token():
    # Firebase CLI session file
    firebase_config_path = os.path.expanduser("~/.config/firebase")
    try:
        with open(firebase_config_path, "r") as file:
            config = json.load(file)
            return config.get("tokens", {}).get("refresh_token", None)
    except FileNotFoundError:
        print("Firebase CLI session file not found. Please log in using `firebase login`.")
        return None
    except json.JSONDecodeError:
        print("Error reading Firebase CLI session file.")
        return None

def get_id_token(refresh_token):
    # Exchange refresh token for an ID token
    token_url = "https://securetoken.googleapis.com/v1/token?key=[FIREBASE_API_KEY]"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("id_token")
    else:
        print(f"Failed to exchange refresh token: {response.text}")
        return None

def authenticate_with_site(id_token):
    api_endpoint = f"{SITE_URL}/api/auth"
    response = requests.post(api_endpoint, json={"idToken": id_token})
    if response.status_code == 200:
        print("Authentication successful!")
        return response.cookies
    else:
        print(f"Authentication failed: {response.text}")
        return None

def open_site_with_session(cookies):
    session = requests.Session()
    session.cookies.update(cookies)
    response = session.get(SITE_URL)
    if response.status_code == 200:
        with open("auth.html", "w") as file:
            file.write(response.text)
        webbrowser.open("auth.html")
    else:
        print(f"Failed to load site: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Authenticate and open site with session details.")
    parser.add_argument("-e", "--email", required=True, help="Email address of the user")
    args = parser.parse_args()

    # Get Firebase CLI token
    refresh_token = get_firebase_cli_token()
    if not refresh_token:
        return

    # Get ID token using the refresh token
    id_token = get_id_token(refresh_token)
    if not id_token:
        return

    # Authenticate with the Next.js site
    cookies = authenticate_with_site(id_token)
    if not cookies:
        return

    # Open the site with session details
    open_site_with_session(cookies)

if __name__ == "__main__":
    main()
