from rich.console import Console
from rich.prompt import Prompt
import requests
from ..session_utils import load_session_details
from ..constants import API_URL

console = Console()

def group_privacy_command():
    """
    Command to update group privacy settings.
    """
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = f"{API_URL}/auth/group/privacy"
    headers = {"Authorization": session_details["token"], "Content-Type": "application/json"}

    # Prompt the user for the group ID and privacy setting
    group_id = Prompt.ask("[bold cyan]Enter the Group ID to update privacy[/]")
    privacy = Prompt.ask(
        "[bold cyan]Set group privacy to [green]private[/] or [blue]public[/][/]", choices=["private", "public"]
    ).lower()

    # Payload for the API
    payload = {"group_id": group_id, "privacy": privacy}

    try:
        response = requests.patch(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            console.print(f"[bold green]✅ Group privacy updated to '{privacy}' successfully![/]")
        else:
            error_message = response.json().get("message", "Unknown error occurred.")
            console.print(f"[bold red]❌ Failed to update group privacy: {error_message}[/]")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
