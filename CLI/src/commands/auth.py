import webbrowser
from flask import Flask, Blueprint, request, redirect
from rich.console import Console
from ..session_utils import save_session_details, load_session_details
import threading
import os
import sys
import time

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
    else:
        console.print("[bold red]❌ Invalid or empty session details, skipping update.")

    # Exit the server after completing the task
    shutdown_flag_file = "shutdown_flag.tmp"
    open(shutdown_flag_file, "w").close()  # Create a flag file to signal shutdown
    return redirect("https://cas.upayan.dev/auth/connect/success")

@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200

def run_server():
    app.register_blueprint(auth_bp)
    app.run(port=8000, use_reloader=False)  # Disable reloader to prevent duplicate shutdown signals

def is_user_authenticated():
    session_details = load_session_details()
    return session_details is not None

def auth_command():
    if is_user_authenticated():
        console.print("[bold green]✔ User is already authenticated. Proceed with your command.")
        return

    url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
    webbrowser.open(url)
    console.print("[bold green]Starting server on [link=http://localhost:8000]http://localhost:8000[/link]")

    # Start the Flask server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    shutdown_flag_file = "shutdown_flag.tmp"

    try:
        while True:
            if os.path.exists(shutdown_flag_file):
                os.remove(shutdown_flag_file)  # Cleanup the flag file
                console.print("[bold purple]Authorization completed!")
                console.print("[bold green]✔ Authentication server terminated. You may now use the CLI.")
                os._exit(0)  # Terminate the program
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[bold red]❌ Server interrupted by user.")
        os._exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Error: {str(e)}")
        os._exit(1)
