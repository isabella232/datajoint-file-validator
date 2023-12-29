from pathlib import Path
from .base_settings import BaseSettings


class Config(BaseSettings):
    """Config class for the application. Mimics behavior of Pydantic's BaseSettings."""

    ENV_PATH = ".env"

    allow_eval: bool = True
    debug: bool = True
    enable_path_handle: bool = True
    default_query: str = "**"
    manifest_schema_parts: Path = Path(
        "datajoint_file_validator/manifest_schemas/parts"
    )
    manifest_schema: Path = Path(
        "datajoint_file_validator/manifest_schemas/latest.yaml"
    )


config = Config()
