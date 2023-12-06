import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

ENABLE_PATH_HANDLE = True


@dataclass
class FileMetadata:
    """Metadata for a file."""
    name: str
    path: str
    abs_path: str
    size: int
    type: str
    mtime_ns: int
    ctime_ns: int
    atime_ns: int
    _path: Optional[Path] = field(default=None, repr=False)

    def __post_init__(self):
        # self.id = f'{self.phrase}_{self.word_type.name.lower()}'
        pass

    @classmethod
    def from_path(cls, path: Path) -> "FileMetadata":
        """Return a FileMetadata object from a Path object."""
        return cls(
            name=path.name,
            path=str(path.relative_to(path.parent)),
            abs_path=str(path),
            size=path.stat().st_size,
            type="file" if path.is_file() else "directory",
            mtime_ns=path.stat().st_mtime_ns,
            ctime_ns=path.stat().st_ctime_ns,
            atime_ns=path.stat().st_atime_ns,
            _path=path if ENABLE_PATH_HANDLE else None,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(path={self.path!r})"

    @staticmethod
    def dict_factory(x):
        exclude_fields = ("_path",)
        return {k: v for (k, v) in x if ((v is not None) and (k not in exclude_fields))}

    def asdict(self):
        return asdict(self, dict_factory=self.dict_factory)


# Define type aliases
S3URI = str
PathLike = Union[str, Path, S3URI]
Snapshot = List[FileMetadata]


def snapshot_posix(path: str) -> Snapshot:
    """Generate a snapshot of a file or directory at local `path`."""
    root = Path(path)
    if root.is_file():
        files = [FileMetadata.from_path(root)]
    elif root.is_dir():
        files = [FileMetadata.from_path(p) for p in root.glob("**/*")]
    else:
        raise ValueError(f"path {path} is not a file or directory")
    return files


def snapshot(path: str) -> Snapshot:
    return snapshot_posix(path)
