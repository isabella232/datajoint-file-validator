import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

# Define type aliases
S3URI = str
PathLike = Union[str, Path, S3URI]
Snapshot = List[Dict[Union[PathLike], Any]]


def snapshot_posix(path: str) -> Snapshot:
    """Generate a snapshot of a file or directory at local `path`."""
    root = Path(path)
    if root.is_file():
        results = [root.relative_to(root)]
    elif root.is_dir():
        results = [p.relative_to(root) for p in root.glob('**/*')]
    else:
        raise ValueError(f'path {path} is not a file or directory')
    return results


def snapshot(path: str) -> Snapshot:
    return snapshot_posix(path)
