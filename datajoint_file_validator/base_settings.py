import os
from typing import Optional, Dict, Any
from dotenv import dotenv_values


class BaseSettings:
    """Settings class for an application. Mimics Pydantic's BaseSettings."""

    ENV_PATH = ".env"

    # Define settings attributes here
    # my_config_val: str = "default value"
    # my_flag: bool = False # setting MY_FLAG=1 in .env will set this to True

    @staticmethod
    def _cast_val(val: str, type_annot: Optional[Any]) -> Any:
        """
        Cast a string `val` to the type of `type_annot`.
        """
        if type_annot is None:
            return val
        if type_annot is bool:
            if val.lower() in ["true", "1"]:
                return True
            elif val.lower() in ["false", "0"]:
                return False
            else:
                raise ValueError(f"Cannot parse '{val}' as bool.")
        try:
            return type_annot(val)
        except ValueError as e:
            raise ValueError(f"Cannot parse '{val}' as {type_annot}.") from e

    def _populate_from_dot_env(self, env_path: str):
        """
        Set attributes from a .env file at `env_path`.
        """
        d = dotenv_values(env_path)
        self._populate_from_dict(d)

    def _populate_from_env_vars(self):
        """
        Set attributes from environment variables.
        """
        d = os.environ
        self._populate_from_dict(d)

    def _populate_from_dict(self, d: Dict[str, Any]):
        """
        Set attributes from a dictionary `d`.
        Skips attributes that are upper-cased, start with an underscore,
        are callable, have no type annotation, or are not class attributes.
        """
        for k, v in self.__class__.__dict__.items():
            val_from_dict = d.get(k.upper(), None)
            type_annot = self.__class__.__annotations__.get(k, None)
            if (
                k.startswith("_")
                or callable(v)
                or k.upper() == k
                or type_annot is None
                or val_from_dict is None
            ):
                continue
            try:
                setattr(self, k, self.cast_val(v, type_annot))
            except ValueError as e:
                raise ValueError(
                    f"Error parsing {k}={val_from_dict} as {type_annot}: {e}"
                ) from e

    def __init__(self, env_path: Optional[str] = None, values: Optional[Dict] = None):
        env_path = env_path or self.ENV_PATH
        if os.path.isfile(env_path):
            self._populate_from_dot_env(env_path)
        self._populate_from_env_vars()
        if values:
            self._populate_from_dict(values)
