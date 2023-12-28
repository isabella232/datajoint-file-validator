from dataclasses import dataclass


@dataclass
class Config:
    """Config class for the application"""

    allow_eval: bool = True
    debug: bool = True
    enable_path_handle: bool = True
    default_query: str = "**"


config = Config()
