from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import itertools
import yaml
from .snapshot import PathLike, FileMetadata
from .query import Query, GlobQuery, DEFAULT_QUERY
from .yaml import read_yaml
from .constraint import Constraint, CONSTRAINT_MAP
from .error import DJFileValidatorError
from .result import ValidationResult
from .snapshot import Snapshot
from .config import config


@dataclass
class Rule:
    """A single rule for a fileset."""

    id: Optional[str]  # TODO: hash by default
    description: Optional[str]
    constraints: List[Constraint] = field(default_factory=list)
    query: Query = field(default_factory=GlobQuery)

    def validate(self, snapshot: Snapshot) -> Dict[str, ValidationResult]:
        filtered_snapshot: Snapshot = self.query.filter(snapshot)
        if self.query.path == DEFAULT_QUERY and config.debug:
            assert filtered_snapshot == snapshot
        results = list(
            map(lambda constraint: constraint.validate(snapshot), self.constraints)
        )
        return {
            constraint.name: result
            for constraint, result in zip(self.constraints, results)
        }

    @staticmethod
    def compile_query(raw: Any) -> "Query":
        assert isinstance(raw, str)
        return GlobQuery(path=raw)

    @staticmethod
    def compile_constraint(name: str, val: Any) -> "Constraint":
        if name not in CONSTRAINT_MAP:
            raise DJFileValidatorError(f"Unknown constraint: {name}")
        try:
            constraint = CONSTRAINT_MAP[name](val)
            constraint._name = name
            return constraint
        except DJFileValidatorError as e:
            raise DJFileValidatorError(f"Error parsing constraint {name}: {e}")

    @classmethod
    def from_dict(cls, d: Dict, check_syntax=False) -> "Rule":
        """Load a rule from a dictionary."""
        if check_syntax:
            assert cls.check_valid(d)
        id = d.pop("id")
        try:
            self_ = cls(
                id=id,
                description=d.pop("description", None),
                query=cls.compile_query(d.pop("query", DEFAULT_QUERY)),
                constraints=[
                    cls.compile_constraint(name, val)
                    for name, val in d.items()
                ],
            )
        except DJFileValidatorError as e:
            raise DJFileValidatorError(f"Error parsing rule '{id}': {e}")
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
    uri: Optional[str] = None

    @staticmethod
    def check_valid(d: Dict) -> bool:
        """User Cerberus to check if manifest has valid syntax."""
        raise NotImplementedError()

    @classmethod
    def from_yaml(cls, path: PathLike, **kw) -> "Manifest":
        """Load a manifest from a YAML file."""
        return cls.from_dict(read_yaml(path), **kw)

    @classmethod
    def from_dict(cls, d: Dict, check_syntax=False) -> "Manifest":
        """Load a manifest from a dictionary."""
        if check_syntax:
            assert cls.check_valid(d)
        self_ = cls(
            # TODO: hash by default
            id=d["id"],
            uri=d.get("uri"),
            version=d["version"],
            description=d["description"],
            rules=[
                Rule.from_dict(rule, check_syntax=check_syntax) for rule in d["rules"]
            ],
        )
        return self_
