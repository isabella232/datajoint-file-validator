from dataclasses import dataclass
from typing import Dict, Any
import cerberus


@dataclass
class ValidationResult:
    status: bool
    errors: Any

    @classmethod
    def from_validator(cls, v: cerberus.Validator):
        return cls(status=v.status, errors=v.errors)
