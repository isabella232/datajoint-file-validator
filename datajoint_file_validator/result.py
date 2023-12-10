from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import cerberus


@dataclass
class ValidationResult:
    status: bool
    # TODO
    message: Any
    context: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_validator(cls, v: cerberus.Validator):
        return cls(status=v.status, errors=v.errors)

    def __repr__(self):
        return f"ValidationResult(status={self.status}, message={self.message})"

    def __bool__(self) -> bool:
        return self.status
