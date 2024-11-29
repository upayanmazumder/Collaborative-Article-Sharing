import requests
import sys
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

API_BASE_URL = "https://cas.upayan.dev"
LOGIN_ENDPOINT = f"{API_BASE_URL}/auth/login"

class AuthCallbackHandler(BaseHTTPRequestHandler):
    """
    HTTP server handler to capture the authentication token from the callback.
    """
    auth_token = None

    def do_GET(self):
        query = self.path.split("?")[-1]
        params = dict(qc.split("=") for qc in query.split("&"))
        AuthCallbackHandler.auth_token = params.get("token")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h1>Authentication Successful</h1>You can close this tab.")

def authenticate_user(email):
    """
    Initiates browser-based authentication and captures the token via a local HTTP server.
    """
    try:
        print(f"Initiating browser-based authentication for {email}...")

        # Request a login URL from the API
        response = requests.post(LOGIN_ENDPOINT, json={"email": email})
        if response.status_code != 200:
            print(f"Error: {response.json().get('error', 'Failed to initiate login.')}")
            sys.exit(1)

        login_url = response.json().get("loginUrl")
        if not login_url:
            print("Error: Login URL not provided by the server.")
            sys.exit(1)

        # Open the login URL in the default web browser
        webbrowser.open(login_url)

        # Start a local HTTP server to capture the token
        server = HTTPServer(("localhost", 8000), AuthCallbackHandler)
        print("Waiting for authentication callback...")
        server.handle_request()

        # Retrieve the token from the callback
        if AuthCallbackHandler.auth_token:
            print(f"Authentication successful! Token: {AuthCallbackHandler.auth_token}")
        else:
            print("Error: Authentication failed. No token received.")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the API: {e}")
        sys.exit(1)
