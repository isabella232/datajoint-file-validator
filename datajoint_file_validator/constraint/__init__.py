from dataclasses import dataclass
from typing import Any
from ..config import Config

Schema = Any


@dataclass
class Constraint:
    """A single constraint that evaluates True or False for a fileset."""
    pass


@dataclass
class CountMinConstraint(Constraint):
    """Constraint for `count_min`."""
    val: int

    def to_schema(self) -> Schema:
        """Convert this constraint to a Cerberus schema."""
        raise NotImplementedError()
        return {"minlength": self.val}


@dataclass
class CountMinConstraint(Constraint):
    """Constraint for `count_min`."""
    val: int

    def to_schema(self) -> Schema:
        """Convert this constraint to a Cerberus schema."""
        raise NotImplementedError()
        return {"minlength": self.val}


@dataclass
class RegexConstraint(Constraint):
    """Constraint for `regex`."""
    val: str

    def to_schema(self) -> Schema:
        """Convert this constraint to a Cerberus schema."""
        raise NotImplementedError()
        return {"regex": self.val}


@dataclass
class RegexConstraint(Constraint):
    """Constraint for `regex`."""
    val: str

    def to_schema(self) -> Schema:
        """Convert this constraint to a Cerberus schema."""
        raise NotImplementedError()
        return {"regex": self.val}


@dataclass
class EvalConstraint(Constraint):
    """Constraint for `eval`."""
    val: str

    def to_schema(self) -> Schema:
        """Convert this constraint to a Cerberus schema."""
        if not Config.allow_eval:
            raise DJFileValidatorError(
                "Eval constraint is not allowed. "
                "Set `Config.allow_eval = True` to allow."
            )
        raise NotImplementedError()
        return {"custom": self.val}


CONSTRAINT_MAP = {
    "count_min": CountMinConstraint,
    "regex": RegexConstraint,
    "eval": EvalConstraint,
}
