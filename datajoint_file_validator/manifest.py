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

    id: Optional[str]  # TODO: hash by default
    description: Optional[str]
    # root: PathLike
    constraints: List[Constraint] = field(default_factory=list)
    query: Query = field(default_factory=GlobQuery)

    @staticmethod
    def compile_query(raw: Any) -> "Query":
        assert isinstance(raw, str)
        return GlobQuery(path=raw)

    @staticmethod
    def compile_constraint(raw: Any) -> "Constraint":
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: Dict, check_syntax=False) -> "Rule":
        """Load a rule from a dictionary."""
        if check_syntax:
            assert self.check_valid(d)

        self_ = cls(
            id=d.pop("id"),
            description=d.pop("description"),
            query=self.compile_query(d.pop("query")),
            constraints=[self.compile_constraint(d[name]) for name in rest],
        )
        return self_


@dataclass
class Manifest:
    """
    Manifest for a fileset, defining a fileset type.
    This class is responsible for parsing a manifest file, validating its
    syntax, and converting into a query and a set of rules.
    """

    id: str
    version: str
    description: str
    rules: List[Rule] = field(default_factory=list)

    @staticmethod
    def check_valid(d: Dict) -> bool:
        """User Cerberus to check if manifest has valid syntax."""
        raise NotImplementedError()

    @classmethod
    def from_yaml(cls, path: PathLike) -> "Manifest":
        """Load a manifest from a YAML file."""
        return cls.from_dict(read_yaml(path))

    @classmethod
    def from_dict(cls, d: Dict, check_syntax=False) -> "Manifest":
        """Load a manifest from a dictionary."""
        # TODO: preprocess

        if check_syntax:
            assert self.check_valid(d)

        self_ = cls(
            id=d["id"],
            version=d["version"],
            description=d["description"],
            rules=[Rule(check_syntax=check_syntax, **r) for r in d["rules"]],
            query=Query.from_dict(d["query"]),
        )
        return self_
