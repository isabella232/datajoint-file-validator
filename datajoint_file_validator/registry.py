import pathlib
import re
from typing import List, Union, Generator, Tuple, Optional, Dict, Any
from pprint import pformat as pf
from wcmatch.pathlib import Path, GLOBSTAR
from wcmatch.glob import glob
from rich.table import Table
from .manifest import Manifest
from .config import config
from .log import logger
from .error import InvalidManifestError
from . import __path__ as MODULE_HOMES


def _get_try_paths(
    query: Union[str, Path], try_extensions: Tuple = (".yaml",)
) -> Generator[Path, None, None]:
    """
    Given a `query` path, yield possible paths to try to find a manifest file,
    in decreasing order of priority. If query has no extension, try adding
    every extension in `try_extensions` to the end of the query.
    """
    if isinstance(query, str):
        query = Path(query)
    # If the query is a path that exists, then we can just use that.
    yield Path(query)
    # Check the `manifests` folder in the current directory.
    yield (Path("manifests") / Path(query))
    # Check the `manifests` folder in the site packages
    for module_loc in MODULE_HOMES:
        yield (Path(module_loc) / Path("manifests") / Path(query))
    # If query has no extension, try adding .yaml
    if query.suffix != ".yaml":
        # Check if there is a file called `default.yaml`
        # in a subdirectory named `query`
        yield from _get_try_paths(Path(query) / Path("default.yaml"))
        for ext in try_extensions:
            yield from _get_try_paths(Path(str(query) + ext))


def find_manifest(query: str) -> Path:
    """
    Try to find a manifest file on local disk, and if that fails,
    the manifest registry.

    Parameters
    ----------
    query : str
        A string to query the registry with.

    Returns
    -------
    Path
        A resolved path to a manifest file.
    """
    if not isinstance(query, str):
        query = str(query)

    try_paths: List[Path] = list(_get_try_paths(query))
    # Remove duplicates while preserving order
    try_paths = list(dict.fromkeys(try_paths))
    logger.debug(f"Trying paths: {pf(try_paths)}")

    for path in try_paths:
        if path.is_file():
            logger.debug(f"Found manifest file: {path}")
            return path
        else:
            logger.debug(f"No manifest file found at: {path}")
    raise FileNotFoundError(f"Could not find manifest file with query: {query}")


def list_manifests(
    query: Optional[str] = None,
    sort_alpha: Optional[str] = "asc",
    additional_dirs: Optional[list] = None,
) -> List[Dict[str, Any]]:
    """
    List all available manifests.

    Parameters
    ----------
    query : Optional[str], optional
        A regular expression query to filter manifest names, by default None

    Returns
    -------
    List[Dict[str, Any]]
        A list of dicts containing information about each manifest.
    """
    if query is None:
        query = ".+"
    additional_dirs = additional_dirs or list()

    # Get the unique set of possible manifest paths from _get_try_paths
    poss_paths = set()
    for dir in ["*", *[f"{dir}/*" for dir in additional_dirs]]:
        for glob_query in _get_try_paths(dir):
            for path_str in glob(str(glob_query)):
                poss_paths.add(Path(path_str).resolve())
    logger.debug(f"Searching for manifests at the following paths: {pf(poss_paths)}")

    manifests = set()
    for path in poss_paths:
        if path.suffix != ".yaml" or not re.search(query, path.name):
            continue
        try:
            manifest = Manifest.from_yaml(path)
        except InvalidManifestError as e:
            logger.debug(
                f"Could not load manifest at {path} "
                f"due to InvalidManifestError: {e}"
            )
            continue
        else:
            manifest._meta["path"] = str(path)
            manifest._meta["stem"] = str(path.stem)
            manifests.add(manifest)
    manifests = list(manifests)

    if sort_alpha is not None:
        if sort_alpha not in ("asc", "desc"):
            raise ValueError(
                f"sort_alpha must be 'asc' or 'desc', " f"not {sort_alpha}"
            )
        manifests = sorted(manifests, key=lambda m: getattr(m, "id", None))
        if sort_alpha == "desc":
            manifests = list(reversed(manifests))

    return [manifest.to_dict() for manifest in manifests]


def table_from_manifest_list(manifests: List[Dict[str, Any]]) -> Table:
    """
    Create a rich table from a list of manifests' dictionary representations.

    Parameters
    ----------
    manifests : List[Dict[str, Any]]
        A list of manifests.

    Returns
    -------
    Table
        A rich table.
    """
    table = Table(
        show_header=True,
        header_style="bold",
        title="Available Manifests",
        show_lines=True,
    )
    table.add_column("ID")
    table.add_column("Version")
    table.add_column("Description")
    table.add_column("Path", overflow="fold")
    for manifest in manifests:
        table.add_row(
            manifest["id"],
            manifest.get("version"),
            manifest.get("description"),
            manifest["_meta"]["path"],
        )
    return table
