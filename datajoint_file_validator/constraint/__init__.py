import re
from dataclasses import dataclass
from typing import Any, Iterable, Callable, Tuple, List, Dict
from abc import ABC, abstractmethod
from cerberus import Validator
from ..config import config
from ..snapshot import Snapshot
from ..result import ValidationResult
from ..error import DJFileValidatorError

Schema = Any


@dataclass(frozen=True)
class Constraint(ABC):
    """A single constraint that evaluates True or False for a fileset."""

    @abstractmethod
    def validate(self, snapshot: Snapshot) -> ValidationResult:
        """Validate a snapshot against a single constraint."""
        pass

    @property
    def name(self):
        _name = getattr(self, "_name", None)
        return _name if _name is not None else self.__class__.__name__


@dataclass(frozen=True)
class CountMinConstraint(Constraint):
    """Constraint for `count_min`."""

    val: int

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        status = len(snapshot) >= self.val
        return ValidationResult(
            status=status,
            message=None
            if status
            else f"constraint `{self.name}` failed: {len(snapshot)} < {self.val}",
            context=dict(snapshot=snapshot, constraint=self),
        )


@dataclass(frozen=True)
class CountMaxConstraint(Constraint):
    """Constraint for `count_max`."""

    val: int

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        status = len(snapshot) <= self.val
        return ValidationResult(
            status=status,
            message=None
            if status
            else f"constraint `{self.name}` failed: {len(snapshot)} > {self.val}",
            context=dict(snapshot=snapshot, constraint=self),
        )


@dataclass(frozen=True)
class SchemaConvertibleConstraint(Constraint):

    @abstractmethod
    def to_schema(self) -> Schema:
        """
        Convert this constraint to a Cerberus schema that each file in
        the Snapshot will be validated against.
        """
        pass

    @staticmethod
    def _validate_file(schema: Schema, file: dict) -> Validator:
        v = Validator(allow_unknown=True)
        v.validate(file, schema)
        return v

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        """Validate a snapshot against a single constraint."""
        schema: Schema = self.to_schema()
        validators: Iterable[Validator] = list(
            map(lambda file: self._validate_file(schema, file), snapshot)
        )
        status = bool(not any(getattr(validator, "errors", None) for validator in validators))
        return ValidationResult(
            status=status,
            message=None if status
            else {
                file["path"]: validator.errors
                for file, validator in zip(snapshot, validators)
                if validator.errors
            },
            context=dict(snapshot=snapshot, constraint=self),
        )


@dataclass(frozen=True)
class RegexConstraint(SchemaConvertibleConstraint):
    """Constraint for `regex`."""

    val: str

    def to_schema(self) -> Schema:
        """
        Convert this constraint to a Cerberus schema that each file in
        the Snapshot will be validated against.
        """
        return {"path": {"type": "string", "required": True, "regex": self.val}}


@dataclass(frozen=True)
class EvalConstraint(Constraint):
    """Constraint for `eval`."""

    val: str

    @staticmethod
    def _eval_function(definition: str) -> Tuple[Callable, str]:
        # Import function definition into locals
        try:
            exec(definition)
        except Exception as e:
            raise e

        # Parse the function name from the definition
        match = re.search(r"def (\w+)", definition)
        if match:
            function_name = match.group(1)
        else:
            raise ValueError(f"Could not parse function name from '{definition}'")
        assert function_name in locals()
        return locals()[function_name], function_name

    def validate(self, snapshot: Snapshot) -> ValidationResult:
        if not config.allow_eval:
            raise DJFileValidatorError(
                "Eval constraint is not allowed. "
                "Set `Config.allow_eval = True` to allow."
            )
        try:
            function, function_name = self._eval_function(self.val)
        except Exception as e:
            raise DJFileValidatorError(
                f"Error parsing function in '{self.name}' constraint: {type(e).__name__}: {e}"
            ) from e
        try:
            status = function(snapshot)
        except Exception as e:
            raise DJFileValidatorError(
                f"Error was raised while executing validation function "
                f"'{function_name}' in "
                f"constraint '{self.name}': {type(e).__name__}: {e}"
            ) from e
        return ValidationResult(
            status=status,
            message=None
            if status
            else f"constraint `{self.name}` failed: {function_name}(snapshot) returned False",
            context=dict(snapshot=snapshot, constraint=self),
        )


CONSTRAINT_MAP = {
    "count_min": CountMinConstraint,
    "count_max": CountMaxConstraint,
    "regex": RegexConstraint,
    "eval": EvalConstraint,
}

for name, cls in CONSTRAINT_MAP.items():
    cls._name = name
