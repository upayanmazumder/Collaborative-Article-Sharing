import requests
import sys

API_BASE_URL = "https://api.cas.upayan.dev"
SIGNUP_ENDPOINT = f"{API_BASE_URL}/auth/signup"
LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"

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

def login_user(email, password):
    """
    Sends a login request to the API.
    """
    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            print(f"User logged in successfully!\n{response.json()}")
        else:
            print(f"Failed to log in user.\nError: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        sys.exit(1)
