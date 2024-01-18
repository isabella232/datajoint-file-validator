import os
import yaml
from typing import Any
import contextlib
from yamlinclude import YamlIncludeConstructor
from wcmatch import pathlib
from .snapshot import PathLike

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.SafeLoader)


@contextlib.contextmanager
def working_directory(path: pathlib.Path):
    prev_cwd = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def _read_yaml(path: PathLike) -> Any:
    """Read a YAML file from `path`."""
    with path.open("r") as f:
        contents = yaml.safe_load(f)
    # Strangely, yaml.safe_load returns None if the file is empty.
    return contents or {}


def read_yaml(path: PathLike) -> Any:
    """
    Read a YAML file from `path`.

    This function supports use of the `!include` tag to include other YAML files
    in the same directory. The included files are read relative to the directory
    of the file containing the tag.
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    try:
        return _read_yaml(path)
    except FileNotFoundError as e:
        # Try resolving an include relative to the parent directory.
        path = path.absolute()
        try:
            with working_directory(path.parent):
                return _read_yaml(path)
        except FileNotFoundError as e2:
            raise e2 from e