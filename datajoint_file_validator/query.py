import os
from typing import Generator
from dataclasses import dataclass
from pathlib import PurePath
from .snapshot import Snapshot, PathLike
from .path_utils import find_matching_files
from .config import config


@dataclass(frozen=True)
class Query:
    """An object representing a query against a snapshot."""

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query. Virtual method."""
        raise NotImplementedError("Subclass of Query must implement filter() method.")


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
