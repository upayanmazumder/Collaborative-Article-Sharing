import sys
from rich.console import Console
from .commands.auth import auth_command
from .commands.info import info_command
from .commands.help import help_command
from .commands.push import push_command
from .commands.pull import pull_command
from .commands.group_create import group_create_command
from .commands.group_delete import group_delete_command
from .commands.group_privacy import group_privacy_command
from .commands.group_list import group_list_command
from .session_utils import load_session_details
import os

# Initialize Rich Console
console = Console()

API_URL = "https://api.cas.upayan.dev"
if os.getenv("ENV") == "development":
    API_URL = "http://localhost:4000"

def is_user_authenticated():
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first using [bold green]cas auth.[/]")
        return False
    return True

def main():
    if len(sys.argv) < 2:
        help_command()
    else:
        command = sys.argv[1].lower()
        
        # Check authentication for restricted commands
        authenticated_commands = ["push", "pull", "group:create", "group:delete", "group:privacy", "group:list"]
        if command in authenticated_commands and not is_user_authenticated():
            return

        # Command dispatch
        if command == "auth":
            auth_command()
        elif command == "info":
            info_command()
        elif command == "help":
            help_command()
        elif command == "push":
            push_command(sys.argv[2:])
        elif command == "pull":
            pull_command()
        elif command == "group:create":
            group_create_command()
        elif command == "group:delete":
            group_delete_command()
        elif command == "group:privacy":
            group_privacy_command()
        elif command == "group:list":
            group_list_command()
        else:
            console.print("[bold red]❌ Unknown command. Use 'cas help' for a list of commands.[/]")

if __name__ == "__main__":
    main()
