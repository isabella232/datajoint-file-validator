import yaml
from typing import Any
from .snapshot import PathLike


def read_yaml(path: PathLike) -> Any:
    """Read a YAML file from `path`."""
    if not isinstance(path, str):
        # Cast to string
        path = str(path)
    with open(path, "r") as f:
        contents = yaml.safe_load(f)
    # Strangely, yaml.safe_load returns None if the file is empty.
    return contents or {}
