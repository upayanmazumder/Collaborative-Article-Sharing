import webbrowser
from flask import Flask, Blueprint, request, redirect
from rich.console import Console
from ..session_utils import save_session_details
import threading
import os
import sys
import time
from ..constants import APP_URL

# Flask and Console initialization
app = Flask(__name__)
console = Console()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def handle_auth_response():
    email = request.args.get("email", "")
    token = request.args.get("token", "")

    if email and token:
        session_details = {"email": email, "token": token}
        save_session_details(session_details)
        console.print(f"[bold green]✔ Session details saved")
        console.print(f"[bold blue]Email: [blue]{email}")

        # Signal success by creating a flag file
        with open("success_flag.tmp", "w") as flag_file:
            flag_file.write("success")
        return redirect(f"{APP_URL}/auth/connect/success")
    else:
        console.print("[bold red]❌ Invalid or empty session details.")
        # Signal failure by creating a flag file
        with open("failure_flag.tmp", "w") as flag_file:
            flag_file.write("failure")
        return redirect(f"{APP_URL}/auth/connect/failure")

@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200

def run_server():
    app.register_blueprint(auth_bp)
    app.run(port=8000, use_reloader=False)  # Disable reloader to prevent duplicate shutdown signals
def auth_command():
    url = f"{APP_URL}/auth/connect?redirect_uri=http://localhost:8000"
    webbrowser.open(url)
    console.print("[bold green]Starting server on [link=http://localhost:8000]http://localhost:8000[/link]")

    # Start the Flask server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    shutdown_flag_file = "shutdown_flag.tmp"
    success_flag_file = "success_flag.tmp"
    failure_flag_file = "failure_flag.tmp"

    try:
        while True:
            if os.path.exists(shutdown_flag_file):
                os.remove(shutdown_flag_file)  # Cleanup the flag file

                if os.path.exists(success_flag_file):
                    os.remove(success_flag_file)  # Cleanup the success flag
                    console.print("[bold purple]Authorization completed!")
                    console.print("[bold green]✔ Authentication server terminated. You may now use the CLI.")

                if os.path.exists(failure_flag_file):
                    os.remove(failure_flag_file)  # Cleanup the failure flag
                    console.print("[bold red]❌ Authentication failed.")
                    console.print("[bold yellow]Please log in to the website and try again.")
                
                os._exit(0)  # Terminate the program

            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bold red]❌ Server interrupted by user.")
        os._exit(1)
