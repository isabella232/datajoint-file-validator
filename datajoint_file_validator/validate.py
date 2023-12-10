import yaml
import cerberus
from typing import Dict, Any, Tuple
from .manifest import Manifest, Rule
from .snapshot import Snapshot, create_snapshot, PathLike
from .result import ValidationResult
from .query import DEFAULT_QUERY

ErrorReport = Any


def validate_snapshot(
    snapshot: Snapshot, manifest_path: PathLike, verbose=False, raise_err=False
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
    manifest = Manifest.from_yaml(manifest_path)
    results: List[Dict[str, ValidationResult]] = list(
        map(lambda rule: rule.validate(snapshot), manifest.rules)
    )
    success = all(map(lambda result: all(result.values()), results))

    error_report = []
    for rule, result in zip(manifest.rules, results):
        for constraint, valresult in result.items():
            if valresult.status:
                continue
            error_report.append(
                {
                    "rule": rule.id,
                    "rule_description": rule.description,
                    "constraint": constraint,
                    "errors": valresult.message,
                }
            )
    if verbose and not success:
        print("Validation failed with the following errors:")
        print("--------------------------------------------")
        print(yaml.dump(error_report))
        print("--------------------------------------------")
    if raise_err and not success:
        raise DJFileValidatorError("Validation failed.")
    return success, error_report


def validate_path(
    path: PathLike, manifest_path: PathLike, verbose=False, raise_err=False
) -> ValidationResult:
    """
    Validate a path against a manifest.

    Parameters
    ----------
    path : PathLike
        A path to a file or directory.
    manifest_path : PathLike
        Path to a manifest file.
    verbose : bool
        Print verbose output.
    raise_err : bool
        Raise an error if validation fails.

    Returns
    -------
    result : ValidationResult
            A dictionary with the validation result.
    """
    snapshot = create_snapshot(path)
    return validate_snapshot(
        snapshot, manifest_path, verbose=verbose, raise_err=raise_err
    )
