import yaml
from typing import Dict
from . import Snapshot, snapshot

ValidationResult = Dict


def validate(
    snapshot: Snapshot, manifest: Manifest, verbose=False, raise_err=False
) -> ValidationResult:
    """
    Validate a snapshot against a manifest.

    Parameters
    ----------
    snapshot : Snapshot
            A snapshot dictionary.
    manifest : Manifest
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
    with open(manifest, "r") as f:
        manifest = yaml.safe_load(f)
    result = validate_snapshot(snapshot, manifest, verbose=verbose)
    if verbose:
        print("Validation result:")
        print(result)
    if raise_err and not result["status"]:
        raise ValueError("Validation failed.")
    return result


def validate_path(
    path: PathLike, manifest: Manifest, verbose=False, raise_err=False
) -> ValidationResult:
    """
    Validate a path against a manifest.

    Parameters
    ----------
    path : PathLike
            A path to a file or directory.
    manifest : Manifest
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
    snapshot = snapshot(path)
    return validate(snapshot, manifest, verbose=verbose, raise_err=raise_err)
