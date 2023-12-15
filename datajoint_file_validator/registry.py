import logging
import pathlib
from wcmatch.pathlib import Path
from . import Manifest
from .config import config
from . import __path__ as MODULE_HOMES

logger = logging.getLogger(__name__)


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
    assert not query.endswith('.yml')
    assert not query.endswith('.json')
    if not query.endswith('.yaml'):
        query += '.yaml'
    try_paths = [
        # If the query is a path that exists, then we can just use that.
        Path(query),
        # Check the `manifests` folder in the current directory.
        (Path('manifests') / Path(query)),
        # Check the `manifests` folder in the site packages
        *[
            (Path(module_loc) / Path('manifests') / Path(query))
            for module_loc in MODULE_HOMES
        ]
    ]
    for path in try_paths:
        if path.exists():
            logger.debug(f"Found manifest file: {path}")
            return path
        else:
            logger.debug(f"No manifest file found at: {path}")
    raise FileNotFoundError(f"Could not find manifest file: {query}")
