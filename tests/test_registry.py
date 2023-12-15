import pytest
from pathlib import Path
from yaml import safe_dump
from datajoint_file_validator import registry, Manifest


@pytest.fixture
def example_manifest() -> Manifest:
    return Manifest(
        id='example_manifest',
        version='0.0.1',
        description='An minimal manifest for testing.',
        rules=[],
    )


def test_find_in_current_path(tmpdir, example_manifest):
    path = Path(tmpdir / 'my_manifest.yaml')
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)

    # Add the manifest file
    example_manifest.to_yaml(path)
    resolved = registry.find_manifest(path)
    assert resolved == str(path)

