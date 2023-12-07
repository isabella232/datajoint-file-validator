from dataclasses import dataclass


@dataclass
class Config:
    """Config class for the application"""

    allow_eval: bool = True
