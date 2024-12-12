from rich.console import Console
from rich.table import Table
import requests
from ..session_utils import load_session_details
from ..constants import API_URL

console = Console()

def pull_command():
    session_details = load_session_details()
    if not session_details:
        console.print("[bold red]❌ Error: User is not logged in. Please log in first.[/]")
        return

    api_url = f"{API_URL}/pull"
    headers = {"Authorization": session_details["token"]}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim")
                table.add_column("Article")
                table.add_column("Message", style="italic")

                for i, article_data in enumerate(articles, 1):
                    table.add_row(str(i), article_data.get("article", "N/A"), article_data.get("message", "N/A"))

                console.print("[bold blue]Your Articles:[/]")
                console.print(table)
            else:
                console.print("[bold yellow]⚠ No articles found.[/]")
        else:
            console.print("[bold red]❌ Error retrieving articles. Status code:", response.status_code)
    except requests.RequestException as e:
        console.print(f"[bold red]❌ API Error: {e}[/]")
