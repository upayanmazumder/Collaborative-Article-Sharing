from rich.console import Console
import requests
from session_utils import load_session_details

console = Console()

def group_list_command():
    """
    Command to fetch and display the list of available groups.
    """
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = "https://api.cas.upayan.dev/auth/group/list"
    headers = {"Authorization": session_details["token"]}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            groups = response_data.get("groups", [])

            if not groups:
                console.print("[bold yellow]⚠️ No groups found.[/]")
                return

            console.print("[bold green]✅ Available Groups:[/]")
            for group in groups:
                # Use correct keys from the API response
                group_name = group.get("group_name", "Unknown Group")
                group_id = group.get("id", "Unknown ID")
                console.print(f"- [cyan]{group_name}[/] (ID: [yellow]{group_id}[/])")
        else:
            error_message = response.json().get("message", "Unknown error occurred.")
            console.print(f"[bold red]❌ Failed to fetch groups: {error_message}[/]")
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
