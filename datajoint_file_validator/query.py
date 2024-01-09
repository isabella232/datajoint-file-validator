import os
from typing import Generator, List, Dict, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import PurePath
from enum import Enum
from .snapshot import Snapshot, PathLike
from .path_utils import find_matching_files
from .config import config
from .error import InvalidQueryError


@dataclass(frozen=True)
class Query(ABC):
    """An object representing a query against a snapshot."""

    @abstractmethod
    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query. Virtual method."""
        pass

    def __and__(self, other: "Query") -> "Query":
        """Combine two queries with an AND operator."""
        return CompositeQuery([self, other])


@dataclass(frozen=True)
class GlobQuery(Query):
    """A query that filters based on path. Includes support for glob wildcards."""

    path: str = config.default_query

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query."""
        return list(self._filter_generator(snapshot))

    def _filter_generator(self, snapshot: Snapshot) -> Generator:
        """Filter a Snapshot based on this query. Returns a generator."""
        return find_matching_files(snapshot, self.path)


class FileType(Enum):
    DIRECTORY = "directory"
    FILE = "file"


@dataclass(frozen=True)
class TypeQuery(Query):
    """A query that filters based on type (file or directory)."""

    file_type: Optional[FileType] = None

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query."""
        return list(self._filter_generator(snapshot))

    def _filter_generator(self, snapshot: Snapshot) -> Generator:
        """Filter a Snapshot based on this query. Returns a generator."""
        for metadata in snapshot:
            if self.file_type is None or metadata.get("type") == self.file_type:
                yield metadata


@dataclass(frozen=True)
class CompositeQuery(Query):
    """A with multiple parts, each of which is a query."""

    parts: List[Query] = field(default_factory=list)

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query."""
        for part in self.parts:
            snapshot = part.filter(snapshot)
        return snapshot

    def __bool__(self):
        return bool(self.parts)

    @classmethod
    def from_dict(cls, d: Dict) -> "CompositeQuery":
        """Create a CompositeQuery from a dictionary."""
        if not isinstance(d, dict):
            raise InvalidQueryError(f"CompositeQuery must be a dict, not {type(d)}")
        if not d:
            raise InvalidQueryError("CompositeQuery cannot be empty")
        path = d.get("path", config.default_query)
        file_type = d.get("type", None)
        return cls(
            parts=[
                GlobQuery(path=path),
                TypeQuery(file_type=file_type),
            ]
        )
