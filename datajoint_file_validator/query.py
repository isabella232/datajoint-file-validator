from dataclasses import dataclass
from .snapshot import PathLike

DEFAULT_QUERY = "/**"

@dataclass
class Query:
    """An object representing a query against a snapshot."""

    pass


@dataclass
class GlobQuery(Query):
    """A query that filters based on path. Includes support for glob wildcards."""

    path: str = "/**"
