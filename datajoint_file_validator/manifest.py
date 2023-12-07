from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import yaml
from .snapshot import PathLike
from .query import Query, GlobQuery
from .yaml import read_yaml


@dataclass
class Constraint:
    """A single constraint that evaluates True or False for a fileset."""
    operator: str


@dataclass
class Rule:
    """A single rule for a fileset."""
    id: Optional[str]
    description: Optional[str]
    # root: PathLike
    constraints: List[Constraint]



@dataclass
class Manifest:
    """Manifest for a fileset, defining a fileset type."""

    id: str
    version: str
    description: str
    rules: List[Rule]
    query: Query = field(default_factory=GlobQuery)

    @classmethod
    def from_yaml(cls, path: PathLike) -> "Manifest":
        """Load a manifest from a YAML file."""
        # self_ = cls.from_dict(read_yaml(path))
        self_ = cls.from_dict({})
        return self_
