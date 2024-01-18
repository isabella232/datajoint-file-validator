from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .constraint import Constraint, CONSTRAINT_MAP
from .result import ValidationResult
from .snapshot import Snapshot, PathLike, FileMetadata
from .query import Query, GlobQuery, CompositeQuery
from .config import config
from .error import InvalidRuleError, InvalidQueryError
from .hash_utils import generate_id


@dataclass
class Rule:
    """A single rule for a fileset."""

    id: Optional[str]
    description: Optional[str]
    constraints: List[Constraint] = field(default_factory=list)
    query: Query = field(default_factory=GlobQuery)

    def __post_init__(self):
        if not self.id:
            self.id = generate_id(self)

    def __hash__(self):
        return hash((self.id, self.query, tuple(self.constraints)))

    def validate(self, snapshot: Snapshot) -> Dict[str, ValidationResult]:
        filtered_snapshot: Snapshot = self.query.filter(snapshot)
        results = list(
            map(
                lambda constraint: constraint.validate(filtered_snapshot),
                self.constraints,
            )
        )
        return {
            constraint.name: result
            for constraint, result in zip(self.constraints, results)
        }

    @staticmethod
    def compile_query(raw: Any) -> "Query":
        if isinstance(raw, dict):
            try:
                return CompositeQuery.from_dict(raw)
            except InvalidQueryError as e:
                raise InvalidRuleError(f"Error parsing query: {e}") from e
        elif not isinstance(raw, str):
            raise InvalidRuleError(f"Query must be a string, not '{type(raw)}'")
        return GlobQuery(path=raw)

    @staticmethod
    def compile_constraint(
        name: str, val: Any, constraint_map=CONSTRAINT_MAP
    ) -> "Constraint":
        if name not in constraint_map:
            raise InvalidRuleError(f"Unknown constraint: '{name}'")
        try:
            return constraint_map[name](val)
        except Exception as e:
            raise InvalidRuleError(f"Error parsing constraint '{name}': {e}") from e

    @classmethod
    def from_dict(cls, d: Dict) -> "Rule":
        """Load a rule from a dictionary."""
        rest = {
            k: v
            for k, v in d.items()
            if k not in ("id", "description", "query", "constraints")
        }
        try:
            self_ = cls(
                id=d.get("id"),
                description=d.get("description"),
                query=cls.compile_query(d.get("query", config.default_query)),
                constraints=[
                    cls.compile_constraint(name, val) for name, val in rest.items()
                ],
            )
        except InvalidRuleError as e:
            raise InvalidRuleError(f"Error parsing rule '{id}': {e}") from e
        return self_
