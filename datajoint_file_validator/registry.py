import pathlib
from typing import List, Union, Generator, Tuple
from pprint import pformat as pf
from wcmatch.pathlib import Path
from . import Manifest
from .config import config
from . import logger, __path__ as MODULE_HOMES


def _get_try_paths(query: Union[str, Path], try_extensions: Tuple = ('.yaml',)) -> Generator[Path, None, None]:
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
    yield (Path('manifests') / Path(query))
    # Check the `manifests` folder in the site packages
    for module_loc in MODULE_HOMES:
        yield (Path(module_loc) / Path('manifests') / Path(query))
    # If query has no extension, try adding .yaml
    if query.suffix != '.yaml':
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
        try:
            query = str(query)
        except Exception as e:
            raise ValueError(
                f"Could not convert query='{query}' to string"
            ) from e

    try_paths: List[Path] = list(_get_try_paths(query))
    if not query.endswith('.yaml'):
        # Check if there is a file called `default` or `default.yaml`
        # in a subdirectory named `query`
        try_paths.extend(_get_try_paths(Path(query) / Path('default')))
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
