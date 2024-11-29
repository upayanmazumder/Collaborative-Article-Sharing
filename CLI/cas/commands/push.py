from rich.console import Console
import requests
from session_utils import load_session_details, is_valid_url

console = Console()

def push_command(args):
    if len(args) < 1:
        console.print("[bold red]Usage: cas push <article-link> [-m <message>][/] ")
        return

    article = None
    message = None

    if "-m" in args:
        m_index = args.index("-m")
        article = " ".join(args[:m_index])
        message = " ".join(args[m_index + 1:])
    else:
        article = " ".join(args)

    if not is_valid_url(article):
        console.print("[bold red]❌ Error: The provided article is not a valid link.[/]")
        return

    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = "https://api.cas.upayan.dev/push"
    headers = {"Authorization": session_details["token"]}
    payload = {"article": article}
    if message:
        payload["message"] = message

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200 and response.json().get("success"):
            console.print("[bold green]✔ Article added successfully![/]")
        else:
            console.print(f"[bold red]❌ Failed to add article: {response.text}")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
