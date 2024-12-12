from rich.console import Console
from rich.text import Text

console = Console()

def help_command():
    help_text = Text("""
Usage:
    cas info                                    Show project and developer information.
    cas help                                    Show this help article.
    cas auth                                    Start authentication process.
    cas push <article-link> [-m <message>]      Add an article with an optional message.
    cas pull                                    Retrieve your articles.
    cas group:create                            Create a group.
    cas group:delete                            Delete a group.
    cas group:privacy                           Change group privacy
    cas group:list                              List all groups.
""", style="bold cyan")
    console.print(help_text)
