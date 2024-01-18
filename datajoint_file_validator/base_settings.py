import os
from typing import Optional, Dict, Any, Union, get_type_hints, get_args, get_origin
from dotenv import dotenv_values


class BaseSettings:
    """Settings class for an application. Mimics Pydantic's BaseSettings."""

    ENV_PATH = ".env"

    # Define settings attributes here
    # my_config_val: str = "default value"
    # my_optional_attr: Optional[str] = None

    # Setting MY_FLAG=1 in .env will set this to True
    # my_flag: bool = False

    # Setting env var MY_CASTED_ATTR='4' will try to cast this as int first, then str
    # my_casted_attr: Union[int, str] = 2

    @staticmethod
    def _cast_val(val: str, type_annot: Optional[Any]) -> Any:
        """
        Cast a string `val` to the type of `type_annot`.
        """
        if val is None:
            return None
        if type_annot is None:
            return val
        if type_annot is bool:
            if str(val).lower() in ["true", "1"]:
                return True
            elif str(val).lower() in ["false", "0"]:
                return False
            else:
                raise ValueError(f"Failed to parse '{val}' as bool.")

        # Handle generic types
        if get_origin(type_annot) is Union:  # includes Optional
            for constr in get_args(type_annot):
                try:
                    return constr(val)
                except (TypeError, ValueError):
                    continue
        elif get_origin(type_annot) is not None:
            raise TypeError(
                f"Cannot parse '{val}' as instance of '{type_annot.__name__}'."
            )
        else:
            constr = type_annot

        # Cast to type
        try:
            return constr(val)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Failed to parse '{val}' as instance of '{type_annot.__name__}'."
            ) from e

    def _populate_from_dot_env(self, env_path: str):
        """
        Set attributes from a .env file at `env_path`.
        """
        d = dotenv_values(env_path)
        self._populate_from_dict(d, match_upper=True)

    def _populate_from_env_vars(self):
        """
        Set attributes from environment variables.
        """
        d = os.environ
        self._populate_from_dict(d, match_upper=True)

    def _populate_from_dict(self, d: Dict[str, Any], match_upper: bool = False):
        """
        Set attributes from a dictionary `d`.
        Skips setting attributes that are upper-cased, start with an underscore,
        are callable, have no type annotation, or are not class attributes.
        """
        attrs = {
            **get_type_hints(self),
            # Include attribute names that have no type annotation but a default value
            **self.__class__.__dict__,
        }
        for k in attrs:
            key_in_d = k.upper() if match_upper else k
            if (
                k.upper() == k
                or k.startswith("_")
                or callable(getattr(self, k, None))
                or key_in_d not in d
            ):
                continue
            val = d[key_in_d]

            type_annot = get_type_hints(self).get(k)
            try:
                setattr(self, k, self._cast_val(val, type_annot))
            except (TypeError, ValueError) as e:
                raise ValueError(
                    f"Error parsing {key_in_d}={val} as {type_annot}: {e}"
                ) from e

    def __init__(self, env_path: Optional[str] = None, **values):
        """
        Create a new settings object, which allows settings to imported from
        environment variables, .env files, and keyword arguments, and accessed
        as attributes. Attributes will be set in the following order:

        1. From default values set in the class definition.
        2. From a .env file at `env_path` (default: `.env`)
        3. From environment variables. Environment variables are matched to
           attributes by upper-casing the attribute name. e.g. to set the
           attribute `my_attr`, set the environment variable `MY_ATTR`.
        4. From keyword arguments passed as `**values` to this constructor.

        The successive step will overwrite any previously set attributes.
        Attribute names that are upper-cased in the class definition, start
        with an underscore, are callable, have no type annotation, or are not
        class attributes will be ignored.

        Parameters
        ----------
        env_path : str
            Path to a .env file. Will be set to `.env` by default.
        **values : Any
            Keyword arguments to set as attributes.
        """
        if not hasattr(self, "__annotations__"):
            self.__annotations__ = {}

        self._populate_from_dict(self.__class__.__dict__)  # From default values
        env_path = env_path or self.ENV_PATH
        if os.path.isfile(env_path):
            self._populate_from_dot_env(env_path)
        self._populate_from_env_vars()
        if values:
            self._populate_from_dict(values)

        # Check that all attributes have been set
        unset_attrs = []
        for k in get_type_hints(self):
            if k.upper() == k or k.startswith("_"):
                continue
            if not hasattr(self, k):
                unset_attrs.append(k)
        if unset_attrs:
            raise ValueError(f"Missing values for attributes: {unset_attrs}")
