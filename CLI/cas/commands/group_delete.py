from rich.console import Console
from rich.prompt import Prompt
import requests
from session_utils import load_session_details

console = Console()

def group_delete_command():
    """
    Command to delete a group.
    """
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = "https://api.cas.upayan.dev/auth/group/delete"
    headers = {"Authorization": session_details["token"], "Content-Type": "application/json"}

    # Prompt the user for the group ID
    group_id = Prompt.ask("[bold cyan]Enter the Group ID to delete[/]")

    # Payload for the API
    payload = {"group_id": group_id}

    try:
        response = requests.delete(api_url, headers=headers, json=payload)
        if response.status_code in [200, 204]:
            console.print(f"[bold green]✅ Group deleted successfully![/]")
        else:
            error_message = response.json().get("message", "Unknown error occurred.")
            console.print(f"[bold red]❌ Failed to delete group: {error_message}[/]")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
