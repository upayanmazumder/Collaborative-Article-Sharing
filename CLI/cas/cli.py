import argparse
import requests
import sys

API_BASE_URL = "https://api.cas.upayan.dev"
SIGNUP_ENDPOINT = f"{API_BASE_URL}/auth/signup"

def signup_user(email, password):
    """
    Sends a signup request to the API.
    """
    try:
        response = requests.post(
            SIGNUP_ENDPOINT,
            json={"email": email, "password": password},
        )
        if response.status_code == 201:
            print(f"User signed up successfully!\n{response.json()}")
        else:
            print(f"Failed to sign up user.\nError: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="CLI tool for signing up users.")
    parser.add_argument(
        "action",
        choices=["signup"],
        help="Action to perform. Currently supports only 'signup'."
    )
    parser.add_argument("-e", "--email", required=True, help="Email address of the user.")
    parser.add_argument("-p", "--password", required=True, help="Password for the user.")
    args = parser.parse_args()

    if args.action == "signup":
        signup_user(args.email, args.password)
