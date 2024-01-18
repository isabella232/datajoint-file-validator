import pytest
import os
from typing import Optional, Union, Callable
from pathlib import Path
from datajoint_file_validator.base_settings import BaseSettings


@pytest.fixture
def example_settings_cls():
    class ExampleSettings(BaseSettings):
        _not_me: str
        _not_me_either: int
        NOT_THIS_ONE: bool = False
        WONT_REGISTER_AS_ATTR: bool
        my_str: str = "default"
        no_annot = "foobar"
        none_val: Optional[str]
        none_val2: Union[None, str]
        none_val3: Optional[str] = None
        my_flag: bool
        my_other_flag: bool = True
        my_false_flag: bool = "0"
        my_path: Path
        my_path_with_default: Path = Path("./my/path/with/default")
        my_path_cast: Path = "./my/path"
        my_optional_str: Optional[str] = None

        def my_method(self) -> str:
            return "foobar"

    return ExampleSettings


@pytest.fixture
def values_dict():
    return {
        "NOT_THIS_ONE": True,
        "my_str": "my_str",
        "my_flag": "1",
        "my_other_flag": "0",
        "my_false_flag": "1",
        "none_val3": "barbaz",
        "my_path": "./my/path",
        "my_path_with_default": "my/other/path",
        "my_path_cast": "./my/other/path",
        "my_optional_str": 12,
    }


def test_can_create_from_parent():
    settings = BaseSettings()
    assert settings


def test_annotations_cast(example_settings_cls):
    settings = example_settings_cls(
        none_val=None,
        none_val2=None,
        none_val3=None,
        my_flag="true",
        my_path="my/path/",
    )
    assert settings.none_val is None
    assert settings.none_val2 is None
    assert settings.none_val3 is None
    assert settings.my_flag is True
    assert settings.my_other_flag is True
    assert settings.my_false_flag is False
    assert settings.my_path == Path("./my/path")
    assert settings.my_path_with_default == Path("./my/path/with/default")
    assert settings.my_path_cast == Path("./my/path")
    assert isinstance(settings.my_method, Callable)


def test_populate_from_dict(example_settings_cls, values_dict):
    settings = example_settings_cls(
        none_val=None,
        none_val2=None,
        none_val3="foobar",
        my_flag="0",
        my_path="my/path",
    )

    assert settings.my_optional_str is None
    assert settings.none_val is None
    assert settings.none_val2 is None
    assert settings.none_val3 is "foobar"
    assert settings.my_flag is False

    settings._populate_from_dict(values_dict)

    assert not hasattr(settings, "WONT_REGISTER_AS_ATTR")
    assert settings.NOT_THIS_ONE is False
    assert settings.my_str == "my_str"
    assert settings.my_flag is True
    assert settings.my_other_flag is False
    assert settings.my_false_flag is True
    assert settings.none_val3 is "barbaz"
    assert settings.my_path == Path("./my/path")
    assert settings.my_path_with_default == Path("./my/other/path")
    assert settings.my_path_cast == Path("my/other/path/")
    assert settings.my_optional_str == "12"

    # Test that we can't set attributes that aren't defined in the class
    settings._populate_from_dict({"foobar": "baz"})
    assert not hasattr(settings, "foobar")

    # Test failed casts
    with pytest.raises(ValueError):
        settings._populate_from_dict({"my_flag": "foobar"})
    with pytest.raises(ValueError):
        settings._populate_from_dict({"my_path": True})


def test_populate_from_env_vars(example_settings_cls, values_dict, monkeypatch):
    settings = example_settings_cls(
        none_val=None, none_val2=None, my_flag="0", my_path="my/path"
    )

    assert settings.my_optional_str is None
    assert settings.none_val is None
    assert settings.none_val2 is None
    assert settings.my_flag is False

    for key, val in values_dict.items():
        monkeypatch.setenv(key.upper(), str(val))
    settings._populate_from_env_vars()

    assert not hasattr(settings, "WONT_REGISTER_AS_ATTR")
    assert settings.NOT_THIS_ONE is False
    assert settings.my_str == "my_str"
    assert settings.my_flag is True
    assert settings.my_other_flag is False
    assert settings.my_false_flag is True
    assert settings.my_path == Path("./my/path")
    assert settings.my_path_with_default == Path("./my/other/path")
    assert settings.my_path_cast == Path("my/other/path/")
    assert settings.my_optional_str == "12"


def test_populate_from_dotenv(example_settings_cls, values_dict, tmp_path):
    settings = example_settings_cls(
        none_val=None, none_val2=None, my_flag="0", my_path="my/path"
    )

    assert settings.my_optional_str is None
    assert settings.none_val is None
    assert settings.none_val2 is None
    assert settings.my_flag is False

    dotenv_path = tmp_path / ".env"
    with open(dotenv_path, "w") as f:
        for key, val in values_dict.items():
            f.write(f"{key.upper()}={val}\n")
    settings._populate_from_dot_env(dotenv_path)

    assert not hasattr(settings, "WONT_REGISTER_AS_ATTR")
    assert settings.NOT_THIS_ONE is False
    assert settings.my_str == "my_str"
    assert settings.my_flag is True
    assert settings.my_other_flag is False
    assert settings.my_false_flag is True
    assert settings.my_path == Path("./my/path")
    assert settings.my_path_with_default == Path("./my/other/path")
    assert settings.my_path_cast == Path("my/other/path/")
    assert settings.my_optional_str == "12"


def test_init(example_settings_cls, values_dict, tmp_path, monkeypatch):
    """
    Test that values are initialized from default values, .env, env vars,
    and kwargs in that order.
    """
    # Write .env
    dotenv_path = tmp_path / ".env"
    with open(dotenv_path, "w") as f:
        for key, val in values_dict.items():
            f.write(f"{key.upper()}={val}\n")

    # Set env vars
    monkeypatch.setenv("MY_STR", "my_str2")
    monkeypatch.setenv("MY_OPTIONAL_STR", "35")
    monkeypatch.setenv("MY_FALSE_FLAG", "1")

    # Initialize settings with kwargs
    settings = example_settings_cls(
        env_path=dotenv_path,
        none_val=None,
        none_val2=None,
        my_path="my/path",
        my_false_flag=0,
        my_optional_str=120,
    )

    assert not hasattr(settings, "WONT_REGISTER_AS_ATTR")
    assert settings.NOT_THIS_ONE is False
    assert settings.my_str == "my_str2"
    assert settings.my_flag is True
    assert settings.no_annot == "foobar", "default value was overwritten"
    assert settings.my_other_flag is False
    assert settings.my_false_flag is False
    assert settings.my_path == Path("./my/path")
    assert settings.my_path_with_default == Path("./my/other/path")
    assert settings.my_path_cast == Path("my/other/path/")
    assert settings.my_optional_str == "120"


def test_init_raises_for_missing_attributes(example_settings_cls, values_dict):
    """
    Test that ValueError is raised if an attribute with a type hint but
    no default value is not provided in .env, env vars, or kwargs.
    """
    vals = values_dict.copy()
    del vals["my_flag"]
    with pytest.raises(ValueError):
        example_settings_cls(none_val=None, none_val2=None, **vals)
    settings = example_settings_cls(none_val=None, none_val2=None, my_flag="1", **vals)
    assert settings.my_flag is True


def test_cast_val(example_settings_cls):
    # Check bool casting
    assert example_settings_cls._cast_val("1", bool) is True
    assert example_settings_cls._cast_val("0", bool) is False
    assert example_settings_cls._cast_val("true", bool) is True
    assert example_settings_cls._cast_val("false", bool) is False
    with pytest.raises(ValueError):
        example_settings_cls._cast_val("foobar", bool)

    # Test generics
    assert example_settings_cls._cast_val("1", Optional[int]) == 1
    assert example_settings_cls._cast_val("1", Optional[str]) == "1"
    assert example_settings_cls._cast_val("1", Optional[bool]) == True
    assert example_settings_cls._cast_val("1", Union[int, str]) == 1
    assert example_settings_cls._cast_val("1", Union[str, int]) == "1"
    assert example_settings_cls._cast_val("1", Union[str, int, bool]) == "1"
    assert example_settings_cls._cast_val("1", Union[bool, str, int]) == True
    assert example_settings_cls._cast_val("1", Union[str, bool, int]) == "1"
    assert example_settings_cls._cast_val("my/path", Path) == Path("my/path")
    with pytest.raises(TypeError):
        example_settings_cls._cast_val("my/path", Callable) == "my/path"
    assert example_settings_cls._cast_val("my/path", Union[Callable, Path]) == Path(
        "my/path"
    )
    with pytest.raises(TypeError):
        example_settings_cls._cast_val("my/path", Union[Callable, Callable])

    # Test casting to None
    with pytest.raises(TypeError):
        example_settings_cls._cast_val("None", int)
    with pytest.raises(TypeError):
        example_settings_cls._cast_val("None", Optional[int])
    assert example_settings_cls._cast_val("None", Optional[str]) is "None"
    assert example_settings_cls._cast_val("None", Optional[bool]) is True
