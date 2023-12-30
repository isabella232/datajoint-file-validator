import pytest
from pathlib import Path
from datajoint_file_validator.base_settings import BaseSettings


@pytest.fixture
def example_settings_cls():

    class ExampleSettings(BaseSettings):
        _not_me: str
        _not_me_either: int
        NOT_THIS_ONE: bool = False
        WONT_REGISTER_AS_ATTR: bool
        my_str: str = 'default'
        no_annot = 'foobar'
        none_val: None
        my_flag: bool
        my_other_flag: bool = True
        my_false_flag: bool = '0'
        my_path: Path
        my_path_with_default: Path = Path('./my/path/with/default')
        my_path_cast: Path = './my/path'

    return ExampleSettings

def test_can_create_from_parent():
    settings = BaseSettings()
    assert settings

def test_annotations_cast(example_settings_cls):
    settings = example_settings_cls(none_val=None, my_flag=None, my_path='my/path/')
    assert settings.my_flag is False
    assert settings.my_other_flag is True
    assert settings.my_false_flag is False
    assert settings.my_path == Path('./my/path')
    assert settings.my_path_with_default == Path('./my/path/with/default')
    assert settings.my_path_cast == Path('./my/path')

def test_populate_from_dict(example_settings_cls):
    settings = example_settings_cls(none_val=None, my_flag=None, my_path='my/path')
    settings._populate_from_dict({
        'NOT_THIS_ONE': True,
        'my_str': 'my_str',
        'my_flag': '1',
        'my_other_flag': '0',
        'my_false_flag': '1',
        'my_path': './my/path',
        'my_path_with_default': 'my/other/path',
        'my_path_cast': './my/other/path',
    })
    assert not hasattr(settings, 'WONT_REGISTER_AS_ATTR')
    assert settings.NOT_THIS_ONE is False
    assert settings.my_str == 'my_str'
    assert settings.my_flag is True
    assert settings.my_other_flag is False
    assert settings.my_false_flag is True
    assert settings.my_path == Path('./my/path')
    assert settings.my_path_with_default == Path('./my/other/path')
    assert settings.my_path_cast == Path('my/other/path/')