import os
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


def test_find_from_exact_path(tmpdir, example_manifest):
    path = Path(tmpdir / 'my_manifest.yaml')
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)

    # Add the manifest file
    example_manifest.to_yaml(path)
    resolved = registry.find_manifest(path)
    assert str(resolved) == str(path)


def test_find_from_current_dir(tmpdir, monkeypatch, example_manifest):
    og_cwd = os.getcwd()
    monkeypatch.chdir(tmpdir)
    path = 'my_manifest.yaml'
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)

    # Add the manifest file
    example_manifest.to_yaml(path)
    resolved = registry.find_manifest(path)
    assert str(resolved) == str(path)

    monkeypatch.chdir(og_cwd)
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)


def test_find_from_site_pkg(example_manifest):
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest('my_nonexistent_manifest')
    resolved = registry.find_manifest('demo_dlc_v0.1')
