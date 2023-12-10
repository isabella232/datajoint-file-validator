import os
from dataclasses import dataclass
from pathlib import PurePath
from .snapshot import Snapshot, PathLike
from .path_utils import find_matching_files

DEFAULT_QUERY = "**"


@dataclass
class Query:
    """An object representing a query against a snapshot."""

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query. Virtual method."""
        raise NotImplementedError("Subclass of Query must implement filter() method.")


@dataclass
class GlobQuery(Query):
    """A query that filters based on path. Includes support for glob wildcards."""

    path: str = DEFAULT_QUERY

    def filter(self, snapshot: Snapshot) -> Snapshot:
        """Filter a Snapshot based on this query."""
        return list(self._filter_generator(snapshot))

    def _filter_generator(self, snapshot: Snapshot):
        """Filter a Snapshot based on this query. Returns a generator."""
        return find_matching_files(snapshot, self.path)
