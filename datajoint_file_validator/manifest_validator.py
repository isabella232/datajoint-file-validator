from cerberus import Validator, errors
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Generator
from .yaml import read_yaml
from .log import logger
from . import __path__ as MODULE_HOMES


def _get_schema_try_paths(
    query: Union[str, Path], try_extensions: Tuple = (".yaml",)
) -> Generator[Path, None, None]:
    """
    Given a `query` path, yield possible paths to try to find a schema file,
    in decreasing order of priority. If query has no extension, try adding
    every extension in `try_extensions` to the end of the query.
    """
    if isinstance(query, str):
        query = Path(query)
    # If the query is a path that exists, then we can just use that.
    yield Path(query)
    # Check the `manifest_schemas` folder in the current directory.
    yield (Path("manifest_schemas") / Path(query))
    # Check the `manifest_schemas` folder in the site packages
    for module_loc in MODULE_HOMES:
        yield (Path(module_loc) / Path("manifest_schemas") / Path(query))
    # If query has no extension, try adding .yaml
    if query.suffix != ".yaml":
        for ext in try_extensions:
            yield from _get_schema_try_paths(Path(str(query) + ext))


class ManifestValidator(Validator):
    @staticmethod
    def _find_manifest_schema(schema_ref: str):
        for path in _get_schema_try_paths(schema_ref):
            logger.debug(f"Looking for `schema_ref` at path='{path}'")
            if path.is_file():
                return path

    def _validate_schema_ref(self, schema_ref, field, value):
        """
        Custom validation method for `schema_ref` field.
        """
        if not isinstance(value, str):
            self._error(field, f"value of 'schema_ref' must be a string, is type '{type(value)}'")
        schema_path = self._find_manifest_schema(schema_ref)
        if schema_path is None:
            self._error(
                field,
                f"schema file schema_ref='{schema_ref}' not "
                "found. Try setting an absolute path.",
            )
        try:
            schema = read_yaml(Path(schema_path).resolve())
        except Exception as e:
            self._error(
                field,
                f"unable to read schema file at schema_ref='{schema_ref}': {e}"
            )
        allow_unknown: Union[Dict, bool] = schema.pop("allow_unknown", False)
        v = ManifestValidator(schema, allow_unknown=allow_unknown)
        valid = v.validate(value)
        if not valid:
            for k, v in v.errors.items():
                self._error(k, str(v))
