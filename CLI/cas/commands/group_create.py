from rich.console import Console
from rich.prompt import Prompt
import requests
from session_utils import load_session_details

console = Console()

def group_create_command():
    """
    Command to create a group by interacting with the API.
    """
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = "https://api.cas.upayan.dev/auth/group/create"
    headers = {"Authorization": session_details["token"], "Content-Type": "application/json"}

    # Prompt the user for group details
    group_name = Prompt.ask("[bold cyan]Enter the group name[/]")
    description = Prompt.ask("[bold cyan]Enter the group description (optional)[/]", default="")

    # Payload for the API
    payload = {
        "group_name": group_name,
        "description": description
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code in [200, 201]:  # Handle both success codes
            data = response.json()
            if data.get("success", True):  # Assume success if not explicitly specified
                console.print(f"[bold green]✅ Group created successfully![/]")
                console.print(f"[bold magenta]Group ID:[/] {data.get('group_id', 'N/A')}")
            else:
                console.print(f"[bold red]❌ Failed to create group: {data.get('message', 'Unknown error')}[/]")
        else:
            console.print(f"[bold red]❌ Unexpected response. Status code: {response.status_code}[/]")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
