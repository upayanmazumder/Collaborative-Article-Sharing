import sys
from rich.console import Console
from .commands.auth import auth_command
from .commands.logout import logout_command
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
        match command:
            case "auth":
                auth_command()
            case "logout":
                logout_command()
            case "info":
                info_command()
            case "help":
                help_command()
            case "push":
                push_command(sys.argv[2:])
            case "pull":
                pull_command()
            case "group:create":
                group_create_command()
            case "group:delete":
                group_delete_command()
            case "group:privacy":
                group_privacy_command()
            case "group:list":
                group_list_command()
            case _:
                console.print("[bold red]❌ Unknown command. Use 'cas help' for a list of commands.[/]")

if __name__ == "__main__":
    main()
