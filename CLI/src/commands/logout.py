import os
from rich.console import Console
from ..session_utils import load_session_details, clear_session_details

console = Console()

def logout_command():
    # Check if session details exist
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: No active session found. You are not logged in.")
        return

    # Clear session details
    clear_session_details()
    console.print("[bold green]✔ Successfully logged out. Session details removed.")
