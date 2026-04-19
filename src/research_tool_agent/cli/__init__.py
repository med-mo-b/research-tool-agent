import typer
from .commands import chat

app = typer.Typer(help="Research Tool Agent CLI")
app.add_typer(chat, name="chat")