import sys
from rich.console import Console
from commands.auth import auth_command
from commands.info import info_command
from commands.help import help_command
from commands.push import push_command
from commands.pull import pull_command

# Initialize Rich Console
console = Console()

def main():
    if len(sys.argv) < 2:
        help_command()
    else:
        command = sys.argv[1].lower()
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
        else:
            console.print("[bold red]❌ Unknown command. Use 'cas help' for a list of commands.[/]")

if __name__ == "__main__":
    main()
