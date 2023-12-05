import typer
from typing_extensions import Annotated
from rich import print as rprint
from . import app


@app.callback()
def callback():
    """
    Welcome to datajoint-file-validator!
    """


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
        print(f"Config line: {path}")


@app.command()
def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")
