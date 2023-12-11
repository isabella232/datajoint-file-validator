import yaml
import cerberus
from typing import List, Dict, Any, Optional, Union, Tuple
from .manifest import Manifest, Rule
from .snapshot import Snapshot, create_snapshot, PathLike
from .result import ValidationResult
from .query import DEFAULT_QUERY
from rich import print as rprint
from rich.console import Console
from rich.table import Table

ErrorReport = List[Dict[str, Any]]


def validate(
    target: Union[Snapshot, PathLike],
    manifest: Union[PathLike, Manifest],
    verbose=False,
    raise_err=False,
) -> Tuple[bool, ErrorReport]:
    """
    Validate a target against a manifest.

    Parameters
    ----------
    target : PathLike | Snapshot
        A path to a file or directory, or an instance of a Snapshot object.
    manifest : PathLike | Manifest
        Path to a manifest file, or an instance of a Manifest object.
    verbose : bool
        Print verbose output.
    raise_err : bool
        Raise an error if validation fails.

    Returns
    -------
    result : dict
        A dictionary with the validation result.
    """
    # Infer how to fetch manifest
    if isinstance(manifest, Manifest):
        mani = manifest
    elif isinstance(manifest, str):
        mani = Manifest.from_yaml(manifest)
    else:
        raise ValueError("manifest must be a path or Manifest object.")

    # Infer how to create snapshot
    if isinstance(target, str):
        target = create_snapshot(target)

    return validate_snapshot(target, mani, verbose=verbose, raise_err=raise_err)


def table_from_report(report: ErrorReport) -> Table:
    """
    Format a validation report as a rich table.
    """
    columns = [
        "rule",
        "rule_description",
        "constraint_id",
        "constraint_value",
        "errors",
    ]
    col_names = [
        "Rule ID",
        "Rule Description",
        "Constraint ID",
        "Constraint Value",
        "Errors",
    ]
    table = Table(*col_names, show_lines=True)
    for item in report:
        as_tup = tuple(str(item[col]) for col in columns)
        table.add_row(*as_tup)
    return table


def validate_snapshot(
    snapshot: Snapshot,
    manifest: Manifest,
    verbose=False,
    raise_err=False,
    format="table",
) -> Tuple[bool, ErrorReport]:
    """
    Validate a snapshot against a manifest.

    Parameters
    ----------
    snapshot : Snapshot
        A snapshot dictionary.
    manifest_path : PathLike
        Path to a manifest file.
    verbose : bool
        Print verbose output.
    raise_err : bool
        Raise an error if validation fails.

    Returns
    -------
    result : dict
        A dictionary with the validation result.
    """
    results: List[Dict[str, ValidationResult]] = list(
        map(lambda rule: rule.validate(snapshot), manifest.rules)
    )
    success = all(map(lambda result: all(result.values()), results))

    # Generate error report
    error_report = []
    for rule, result in zip(manifest.rules, results):
        for constraint, valresult in result.items():
            if valresult.status:
                continue
            error_report.append(
                {
                    "rule": rule.id,
                    "rule_description": rule.description,
                    "constraint_id": constraint,
                    "constraint_value": valresult.context["constraint"].val,
                    "errors": valresult.message,
                }
            )
    if verbose and not success:
        rprint("Validation failed with the following errors:")
        if format == "table":
            table = table_from_report(error_report)
            console = Console()
            console.print(table)
        elif format == "yaml":
            rprint(yaml.dump(error_report))
        else:
            raise ValuError(f"Unsupported format: {format}")
    if raise_err and not success:
        raise DJFileValidatorError("Validation failed.")

    return success, error_report
