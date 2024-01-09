from pathlib import Path
from .base_settings import BaseSettings
from . import __path__ as MODULE_HOMES


class Config(BaseSettings):
    """Config class for the application. Mimics behavior of Pydantic's BaseSettings."""

    ENV_PATH = ".env"

    allow_eval: bool = True
    debug: bool = True
    enable_path_handle: bool = True
    default_query: str = "**"
    manifest_schema_parts: Path = next(
        Path(module_home) / Path("manifest_schemas/parts")
        for module_home in MODULE_HOMES
        if Path(module_home).is_dir()
    )
    manifest_schema: Path = next(
        Path(module_home) / Path("manifest_schemas/latest.yaml")
        for module_home in MODULE_HOMES
        if Path(module_home).is_dir()
    )


config = Config()
