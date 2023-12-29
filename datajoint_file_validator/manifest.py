from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import yaml
from pprint import pformat as pf
from cerberus import Validator
from .yaml import read_yaml
from .error import DJFileValidatorError, InvalidManifestError
from .result import ValidationResult
from .snapshot import Snapshot, PathLike, FileMetadata
from .config import config
from .rule import Rule
from .hash_utils import generate_id


@dataclass
class Manifest:
    """
    Manifest for a fileset, defining a fileset type.
    This class is responsible for parsing a manifest file, validating its
    syntax, and converting into a query and a set of rules.
    """

    id: Optional[str]
    version: Optional[str] = None
    description: Optional[str] = None
    uri: Optional[str] = None
    rules: List[Rule] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = generate_id(self)

    def __hash__(self):
        return hash((self.id, self.version, tuple(self.rules)))

    @staticmethod
    def check_valid(d: Dict, mani_schema: Path) -> Tuple[bool, Dict]:
        """Use Cerberus to check if manifest has valid syntax."""
        schema: Dict = read_yaml(mani_schema)
        allow_unknown: Union[Dict, bool] = schema.pop("allow_unknown", False)
        v = Validator(schema, allow_unknown=allow_unknown)
        valid = v.validate(d)
        return valid, v.errors

    @classmethod
    def from_yaml(cls, path: PathLike, **kw) -> "Manifest":
        """Load a manifest from a YAML file."""
        try:
            return cls.from_dict(read_yaml(path), **kw)
        except InvalidManifestError as e:
            raise InvalidManifestError(
                f"Error loading manifest at '{path}':\n{e}"
            ) from e

    @classmethod
    def from_dict(cls, d: Dict, check_valid=True) -> "Manifest":
        """Load a manifest from a dictionary."""
        if check_valid:
            mani_schema = config.manifest_schema
            valid, errors = cls.check_valid(d, mani_schema=mani_schema)
            if not valid:
                raise InvalidManifestError(
                    f"Manifest does not match schema at '{mani_schema}' with "
                    f"the following errors:\n{pf(errors, indent=4)}"
                )
        self_ = cls(
            id=d.get("id"),
            uri=d.get("uri"),
            version=d.get("version"),
            description=d.get("description"),
            rules=[Rule.from_dict(rule) for rule in d.get("rules", [])],
        )
        return self_

    def to_dict(self):
        return asdict(self)

    def to_yaml(self, path: PathLike):
        with open(path, "w") as f:
            yaml.safe_dump(self.to_dict(), f)
