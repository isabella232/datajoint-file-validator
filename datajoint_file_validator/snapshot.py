import os
from datetime import datetime
import pytz
from dataclasses import dataclass, field, asdict
from wcmatch import pathlib
from wcmatch.pathlib import Path
from typing import List, Dict, Any, Optional, Union
from .config import config


@dataclass
class FileMetadata:
    """
    Metadata for a file.
    """

    name: str
    path: str = field(init=False)
    abs_path: str
    rel_path: str
    extension: str
    size: int
    type: str
    last_modified: str
    mtime_ns: int
    ctime_ns: int
    atime_ns: int
    _path: Optional[Path] = field(default=None, repr=False)

    def __post_init__(self):
        self.path = self.rel_path

    @staticmethod
    def to_iso_8601(time_ns: int):
        time_ = datetime.fromtimestamp(time_ns / 1e9)
        return time_.replace(tzinfo=pytz.UTC).isoformat()

    @classmethod
    def from_path(cls, path: Path, root: Path) -> "FileMetadata":
        """Return a FileMetadata object from a Path object."""
        is_file = path.is_file()
        rel_path = str(path.relative_to(root))
        abs_path = str(path)
        # Add trailing slash to directories
        if not is_file and not rel_path.endswith("/"):
            rel_path += "/"
            abs_path += "/"

        return cls(
            name=path.name,
            rel_path=rel_path,
            abs_path=abs_path,
            size=path.stat().st_size,
            type="file" if is_file else "directory",
            last_modified=cls.to_iso_8601(path.stat().st_mtime_ns),
            extension=path.suffix,
            mtime_ns=path.stat().st_mtime_ns,
            ctime_ns=path.stat().st_ctime_ns,
            atime_ns=path.stat().st_atime_ns,
            _path=path if config.enable_path_handle else None,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(path={self.path!r}, type={self.type!r})"

    @staticmethod
    def _dict_factory(x):
        exclude_fields = ("_path",)
        return {k: v for (k, v) in x if ((v is not None) and (k not in exclude_fields))}

    def asdict(self):
        return asdict(self, dict_factory=self._dict_factory)


# Define type aliases
S3URI = str
PathLike = Union[str, Path, S3URI]
Snapshot = List[Dict[str, Any]]


def _snapshot_to_cls(
    path: str, flags=(pathlib.GLOBSTAR | pathlib.SPLIT | pathlib.FOLLOW)
) -> List[FileMetadata]:
    """Generate a snapshot of a file or directory at local `path`."""
    root = Path(path)
    if root.is_file():
        files = [FileMetadata.from_path(root, root.parent)]
    elif root.is_dir():
        files = [FileMetadata.from_path(p, root) for p in root.glob("**", flags=flags)]
    else:
        raise ValueError(f"path {path} is not a file or directory")
    return files


def create_snapshot(path: str) -> Snapshot:
    """
    Generate a snapshot of a file or directory at local `path`.
    Converts the list of dataclasses to a Snapshot.
    """
    files = _snapshot_to_cls(path)
    return [f.asdict() for f in files]
