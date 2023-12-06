from dataclasses import dataclass
from typing import Dict, List, Any
from .snapshot import PathLike

Manifest = Any


@dataclass
class Constraint:
    """A single constraint that evaluates True or False for a fileset."""
    operator: str


@dataclass
class Rule:
    """A single rule for a fileset."""
    name: str
    description: str
    root: PathLike
    constraints: List[Constraint]



@dataclass
class Manifest:
    """Manifest for a fileset, defining a fileset type."""

    name: str
    version: str
    description: str
    rules: List[Rule]
