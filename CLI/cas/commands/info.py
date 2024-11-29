from rich.console import Console
from rich.text import Text

console = Console()

def info_command():
    info_text = Text("""
Project Information:
    GitHub Repo: https://github.com/upayanmazumder/Collaborative-Article-Sharing
    PyPI Repo: https://pypi.org/project/collaborative-article-sharing/
    Discord: https://discord.gg/wQTZcXpcaY
    Website: https://cas.upayan.dev

Developer Information:
    Name: Upayan Mazumder
    My Site: https://upayan.dev
""", style="bold yellow")
    console.print(info_text)
