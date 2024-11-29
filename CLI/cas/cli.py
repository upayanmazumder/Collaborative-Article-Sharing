import argparse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json

# Simple HTTP handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = urlparse.urlparse(self.path).query
        params = urlparse.parse_qs(query)

        # Extract session details
        session_details = {
            "email": params.get("email", [""])[0],
            "token": params.get("token", [""])[0]
        }

        # Store session details in a file
        with open("session_details.json", "w") as file:
            json.dump(session_details, file)

        # Send response to the browser
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Authentication Successful!</h1><p>You can close this window.</p>")

        print("Session details saved:", session_details)

def main():
    parser = argparse.ArgumentParser(description="CLI for connecting to cas.upayan.dev.")
    args = parser.parse_args()

    # Start the HTTP server
    server_address = ("localhost", 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on http://localhost:8000")

    # Open the browser
    redirect_url = "http://localhost:8000"
    connect_url = f"https://cas.upayan.dev/auth/connect?redirect_uri={redirect_url}"
    print(f"Opening {connect_url} in the browser...")
    webbrowser.open(connect_url)

    # Run the server
    httpd.serve_forever()

if __name__ == "__main__":
    main()
