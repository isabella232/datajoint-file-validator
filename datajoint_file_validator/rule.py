from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .constraint import Constraint, CONSTRAINT_MAP
from .result import ValidationResult
from .snapshot import Snapshot, PathLike, FileMetadata
from .query import Query, GlobQuery, DEFAULT_QUERY
from .config import config


@dataclass
class Rule:
    """A single rule for a fileset."""

    id: Optional[str]
    description: Optional[str]
    constraints: List[Constraint] = field(default_factory=list)
    query: Query = field(default_factory=GlobQuery)

    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        return hash(self)

    def __hash__(self):
        return hash((self.query, sorted(self.constraints)))

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
        id = d.pop("id", None)
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
