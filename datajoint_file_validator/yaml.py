import yaml
from typing import Any
from .snapshot import PathLike


def read_yaml(path: PathLike) -> Any:
	"""Read a YAML file from `path`."""
	with open(path, "r") as f:
		return yaml.safe_load(f)
