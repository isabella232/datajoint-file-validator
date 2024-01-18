import sys
import json
import typer
from enum import Enum
from typing import List, Dict, Any, Optional
from typing_extensions import Annotated
import yaml
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from . import main, registry

console = Console()
app = typer.Typer()
manifest_app = typer.Typer(name="manifest")
app.add_typer(manifest_app, name="manifest")


@app.callback()
def callback():
    """
    Welcome to datajoint-file-validator!
    """
    pass


class DisplayFormat(str, Enum):
    table = "table"
    yaml = "yaml"
    json = "json"


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
        rprint(":heavy_check_mark: Validation successful!", file=sys.stderr)
        return

    rprint(f":x: Validation failed with {len(report)} errors!", file=sys.stderr)
    if format == DisplayFormat.table:
        table = main.table_from_report(report)
        console = Console()
        console.print(table)
    elif format == DisplayFormat.yaml:
        rprint(file=sys.stderr)
        rprint(yaml.dump(report))
    elif format == DisplayFormat.json:
        rprint(json.dumps(report, indent=2))
    raise typer.Exit(code=1)


@manifest_app.command(name="list")
def list_manifests(
    query: Optional[str] = typer.Option(
        None,
        help="Filter manifest names using this regular expression query",
    ),
    format: DisplayFormat = DisplayFormat.table,
):
    """
    List all available manifests.
    """
    manifests: List[Dict[str, Any]] = registry.list_manifests(query=query)
    if format == DisplayFormat.table:
        table = registry.table_from_manifest_list(manifests)
        console = Console()
        console.print(table)
    elif format == DisplayFormat.yaml:
        rprint(file=sys.stderr)
        rprint(yaml.dump(manifests))
    elif format == DisplayFormat.json:
        rprint(json.dumps(manifests, indent=2))
