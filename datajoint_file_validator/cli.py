import typer
from enum import Enum
from typing_extensions import Annotated
import yaml
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from . import main

console = Console()
app = typer.Typer()


@app.callback()
def callback():
    """
    Welcome to datajoint-file-validator!
    """


def show_table():
    table = Table("Name", "Item")
    table.add_row("Rick", "Portal Gun")
    table.add_row("Morty", "Plumbus")
    console.print(table)


def open_file(path: str):
    """
    Open a file at PATH in the default app.
    """
    rprint(f":left_speech_bubble:  Opening file {path}")
    typer.launch(path, locate=True)


def read_file(path: Annotated[typer.FileText, typer.Option()]):
    """
    Reads lines from a file at PATH.
    """
    for line in path:
        rprint(f"Config line: {path}")


def _main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        rprint(f"Good day Ms. {name} {lastname}.")
    else:
        rprint(f"Hello {name} {lastname}")


class DisplayFormat(str, Enum):
    table = "table"
    yaml = "yaml"
    plain = "plain"


@app.command()
def validate(
    target: Annotated[str, typer.Argument(..., exists=True)],
    manifest: Annotated[str, typer.Argument(..., exists=True)],
    raise_err: bool = False,
    format: DisplayFormat = DisplayFormat.table,
):
    """
    Validate a target against a manifest.
    """
    success, report = main.validate(
        target, manifest, verbose=False, raise_err=raise_err
    )
    if success:
        rprint(":heavy_check_mark: Validation successful!")
        return

    rprint(f":x: Validation failed with {len(report)} errors!")
    if format == DisplayFormat.table:
        table = main.table_from_report(report)
        console = Console()
        console.print(table)
    elif format == DisplayFormat.yaml:
        rprint()
        rprint(yaml.dump(report))
    elif format == DisplayFormat.plain:
        rprint(report)
    raise typer.Exit(code=1)
