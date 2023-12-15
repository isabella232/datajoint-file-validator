from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import yaml
from .yaml import read_yaml
from .error import DJFileValidatorError
from .result import ValidationResult
from .snapshot import Snapshot, PathLike, FileMetadata
from .config import config
from .rule import Rule


@dataclass
class Manifest:
    """
    Manifest for a fileset, defining a fileset type.
    This class is responsible for parsing a manifest file, validating its
    syntax, and converting into a query and a set of rules.
    """

    id: str
    version: Optional[str] = None
    description: Optional[str] = None
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
