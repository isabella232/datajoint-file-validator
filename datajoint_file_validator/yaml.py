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


def _read_yaml(path: pathlib.Path) -> Any:
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
    with working_directory(path.parent):
        return _read_yaml(path.relative_to(path.parent))


def is_reference(path: PathLike) -> bool:
    """
    Determine if a YAML file at `path` contains exactly 1 reference (using
    the `!include` tag) to another YAML file, and nothing else
    (besides comments).
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    n_includes = 0
    with path.open("r") as f:
        for line in f.readlines():
            if line.strip().startswith("#"):
                continue
            if line.strip().startswith("!include"):
                n_includes += 1
    return n_includes == 1