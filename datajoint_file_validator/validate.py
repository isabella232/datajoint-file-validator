import yaml
import cerberus
from typing import Dict
from .manifest import Manifest, Rule
from .snapshot import Snapshot, create_snapshot, PathLike
from .result import ValidationResult
from .query import DEFAULT_QUERY



def validate_snapshot(
    snapshot: Snapshot, manifest_path: PathLike, verbose=False, raise_err=False
) -> ValidationResult:
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
    results = list(map(lambda rule: rule.validate(snapshot), manifest.rules))
    return results


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
