from dataclasses import dataclass
from typing import Any, Iterable
from cerberus import Validator
from ..config import config
from ..snapshot import Snapshot
from ..result import ValidationResult

Schema = Any


@dataclass
class Constraint:
    """A single constraint that evaluates True or False for a fileset."""

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        """Validate a snapshot against a single constraint."""
        raise NotImplementedError("Subclass of Constraint must implement validate() method.")

    @property
    def name(self):
        _name = getattr(self, "_name", None)
        return _name if _name else self.__class__.__name__


@dataclass
class CountMinConstraint(Constraint):
    """Constraint for `count_min`."""
    val: int

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        status = len(snapshot) >= self.val
        return ValidationResult(
            status=status,
            message=None if status else f"constraint `{self.name}` failed: {len(snapshot)} < {self.val}",
            context=dict(snapshot=snapshot, constraint=self)
        )


@dataclass
class CountMaxConstraint(Constraint):
    """Constraint for `count_max`."""
    val: int

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        status = len(snapshot) <= self.val
        return ValidationResult(
            status=status,
            message=None if status else f"constraint `{self.name}` failed: {len(snapshot)} > {self.val}",
            context=dict(snapshot=snapshot, constraint=self)
        )


@dataclass
class SchemaConvertibleConstraint(Constraint):

    def to_schema(self) -> Schema:
        """
        Convert this constraint to a Cerberus schema that each file in
        the Snapshot will be validated against.
        """
        raise NotImplementedError("Subclass of SchemaConvertibleConstraint must implement to_schema() method.")

    @staticmethod
    def _validate_file(schema: Schema, file: dict) -> Validator:
        v = Validator(allow_unknown=True)
        v.validate(file, schema)
        return v

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        """Validate a snapshot against a single constraint."""
        schema: Schema = self.to_schema()
        assert isinstance(schema, dict)
        v = Validator(allow_unknown=True)
        validators: Iterable[Validator] = list(map(lambda file: self._validate_file(schema, file), snapshot))
        return ValidationResult(
            status=all(validators),
            message=None if all(validators) else {
                file["path"]: validator.errors
                for file, validator in zip(snapshot, validators)
            },
            context=dict(snapshot=snapshot, constraint=self)
        )
        breakpoint()
        raise NotImplementedError()


@dataclass
class RegexConstraint(SchemaConvertibleConstraint):
    """Constraint for `regex`."""
    val: str

    def to_schema(self) -> Schema:
        """
        Convert this constraint to a Cerberus schema that each file in
        the Snapshot will be validated against.
        """
        return {
            "path": {
                "type": "string",
                "required": True,
                "regex": self.val
            }
        }




@dataclass
class EvalConstraint(Constraint):
    """Constraint for `eval`."""
    val: str

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        if not config.allow_eval:
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
