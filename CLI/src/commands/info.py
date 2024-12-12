from rich.console import Console
from rich.markdown import Markdown

console = Console()

def info_command():
    info_text = Markdown("""
# **Project Information:**
- [GitHub Repo](https://github.com/upayanmazumder/Collaborative-Article-Sharing)
- [PyPI Repo](https://pypi.org/project/collaborative-article-sharing/)
- [Discord](https://discord.gg/wQTZcXpcaY)
- [Website](https://cas.upayan.dev)

**Made with love by**
[Upayan Mazumder](https://upayan.dev)
""")
    console.print(info_text)

if __name__ == "__main__":
    info_command()
