import os
import json
import webbrowser
import sys
import requests
from flask import Flask, Blueprint, request, jsonify, redirect
import re
from rich.console import Console
from rich.text import Text
from rich.table import Table

# Initialize Rich Console
console = Console()

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

    if email and token:
        session_details = {"email": email, "token": token}
        save_session_details(session_details)
        console.print(f"[bold green]✔ Session details saved")
        console.print(f"[bold blue]Email: [blue]{email}")
        console.print("[bold purple]Authorization completed! [purple] You can now use cas pull,push etc..")
    else:
        console.print("[bold red]❌ Invalid or empty session details, skipping update.")

    return redirect("https://cas.upayan.dev/auth/connect/success")

@auth_bp.route("/favicon.ico")
def favicon():
    return "", 200

def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?:\/\/)?'
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'
        r'([\/\w \.-]*)*\/?$'
    )
    return re.match(url_regex, url) is not None

def add_article(article):
    if not is_valid_url(article):
        console.print("[bold red]❌ Error:[/] The provided article is not a valid link.")
        return

    session_details = load_session_details()
    if not session_details or "email" not in session_details or "token" not in session_details:
        console.print("[bold red]❌ Error:[/] User is not logged in. Please log in first.")
        return

    api_url = "https://api.cas.upayan.dev/push"
    headers = {"Authorization": session_details["token"]}
    payload = {"article": article}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                console.print("[bold green]✔ Article added successfully![/]")
            else:
                console.print(f"[bold red]❌ Failed to add article. Reason:[/] {data.get('message', 'Unknown error.')}")
        else:
            console.print(f"[bold red]❌ Failed to add article. Status Code:[/] {response.status_code}")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ Error while communicating with the API:[/] {e}")

def pull_articles():
    session_details = load_session_details()
    if not session_details or "email" not in session_details or "token" not in session_details:
        console.print("[bold red]❌ Error:[/] User is not logged in. Please log in first.")
        return

    api_url = "https://api.cas.upayan.dev/pull"
    headers = {"Authorization": session_details["token"]}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                console.print("[bold blue]Your Articles:[/]")
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim")
                table.add_column("Article")
                for i, article in enumerate(articles, 1):
                    table.add_row(str(i), article)
                console.print(table)
            else:
                console.print("[bold yellow]⚠ You have no articles.[/]")
        else:
            console.print("[bold red]❌ Failed to retrieve articles. Error:[/]", response.json())
    except requests.RequestException as e:
        console.print(f"[bold red]❌ Error while communicating with the API:[/] {e}")

def show_help():
    help_text = Text("""
Usage:
    cas help                            Show this help article.
    cas auth                            Start authentication process.
    cas push <article-link>             Add an article.
    cas pull                            Retrieve your articles.
""", style="bold cyan")
    console.print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "push":
        if len(sys.argv) < 3:
            console.print("[bold red]Usage: cas push <article-link>[/]")
        else:
            article = " ".join(sys.argv[2:])
            add_article(article)
    elif sys.argv[1] == "pull":
        pull_articles()
    elif sys.argv[1] == "help":
        show_help()
    elif sys.argv[1] == "auth":
        url = "https://cas.upayan.dev/auth/connect?redirect_uri=http://localhost:8000"
        webbrowser.open(url)
        console.print("[bold green]Starting server on [link=http://localhost:8000]http://localhost:8000[/link]")
        app = Flask(__name__)
        app.register_blueprint(auth_bp)
        app.run(port=8000)
    else:
        show_help()

if __name__ == "__main__":
    main()
