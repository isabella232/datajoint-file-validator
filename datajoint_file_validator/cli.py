import typer
from typing_extensions import Annotated
from rich import print as rprint
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.callback()
def callback():
    """
    Welcome to datajoint-file-validator!
    """


@app.command()
def show_table():
    table = Table("Name", "Item")
    table.add_row("Rick", "Portal Gun")
    table.add_row("Morty", "Plumbus")
    console.print(table)


@app.command()
def open_file(path: str):
    """
    Open a file at PATH in the default app.
    """
    rprint(f":left_speech_bubble:  Opening file {path}")
    typer.launch(path, locate=True)


@app.command()
def read_file(path: Annotated[typer.FileText, typer.Option()]):
    """
    Reads lines from a file at PATH.
    """
    for line in path:
        rprint(f"Config line: {path}")


@app.command()
def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        rprint(f"Good day Ms. {name} {lastname}.")
    else:
        rprint(f"Hello {name} {lastname}")
