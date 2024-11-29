import webbrowser
from flask import Flask
from rich.console import Console
from session_utils import save_session_details
from flask import Blueprint, request, redirect

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
        console.print("[bold purple]Authorization completed!")
    else:
        console.print("[bold red]❌ Invalid or empty session details, skipping update.")

    return redirect("https://cas.upayan.dev/auth/connect/success")

@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200

def auth_command():
    url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
    webbrowser.open(url)
    console.print("[bold green]Starting server on [link=http://localhost:8000]http://localhost:8000[/link]")
    app.register_blueprint(auth_bp)
    app.run(port=8000)
