import yaml
from typing import Any
from .snapshot import PathLike
from yamlinclude import YamlIncludeConstructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir='/your/path')


def read_yaml(path: PathLike) -> Any:
    """Read a YAML file from `path`."""
    if not isinstance(path, str):
        # Cast to string
        path = str(path)
    with open(path, "r") as f:
        contents = yaml.load(f, Loader=yaml.FullLoader)
    # Strangely, yaml.safe_load returns None if the file is empty.
    return contents or {}
