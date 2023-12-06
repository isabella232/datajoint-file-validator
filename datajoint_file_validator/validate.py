import yaml
import cerberus
from typing import Dict
from .manifest import Manifest
from .snapshot import Snapshot, snapshot, PathLike
from .result import ValidationResult


def validate_snapshot(
    snapshot: Snapshot, manifest: Manifest, verbose=False, raise_err=False
) -> ValidationResult:
    """
    Validate a snapshot against a manifest.

    Parameters
    ----------
    snapshot : Snapshot
            A snapshot dictionary.
    manifest : Manifest
            Contents of a manifest file.
    verbose : bool
            Print verbose output.
    raise_err : bool
            Raise an error if validation fails.

    Returns
    -------
    result : dict
            A dictionary with the validation result.
    """
    # Convert manifest to Cerberus schema
    raise NotImplementedError()
    # Validate snapshot against schema using Cerberus
    v = cerberus.Validator(schema)
    v.validate(snapshot)
    result = ValidationResult.from_validator(v)
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
