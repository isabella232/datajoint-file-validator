import os
import pytest
from pathlib import Path
from pprint import pformat as pf
from yaml import safe_dump
from datajoint_file_validator import registry, Manifest
from . import logger


@pytest.fixture
def example_manifest() -> Manifest:
    return Manifest(
        id="example_manifest",
        version="0.0.1",
        description="An minimal manifest for testing.",
        rules=[],
    )


def test_find_from_exact_path(tmpdir, example_manifest):
    path = Path(tmpdir / "my_manifest.yaml")
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)

    # Add the manifest file
    example_manifest.to_yaml(path)
    resolved = registry.find_manifest(path)
    assert str(resolved) == str(path)


def test_find_from_current_dir(tmpdir, monkeypatch, example_manifest):
    og_cwd = os.getcwd()
    monkeypatch.chdir(tmpdir)
    path = "my_manifest.yaml"
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)

    # Add the manifest file
    example_manifest.to_yaml(path)
    resolved = registry.find_manifest(path)
    assert str(resolved) == str(path)

    monkeypatch.chdir(og_cwd)
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest(path)


def test_find_from_site_pkg():
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest("my_nonexistent_manifest")
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest("my_nonexistent_manifest.yaml")
    resolved = registry.find_manifest("demo_rnaseq_v0.1")
    resolved = registry.find_manifest("demo_rnaseq_v0.1.yaml")


def test_find_from_site_pkg_symlink():
    """
    Symlink in the manifest directory should resolve correctly.
    """
    resolved = registry.find_manifest("demo_rnaseq")
    assert resolved.resolve().name == "demo_rnaseq_v0.1.yaml"


def test_find_in_subdir_from_site_pkg_symlink():
    """
    Symlink in a subdir within the manifest directory should resolve correctly.
    """
    resolved = registry.find_manifest("demo_dlc")
    assert resolved.name == "default.yaml"
    assert resolved.resolve().name == "v0.1.yaml"
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest("demo_dlc.yaml")


def test_list_manifests_basic():
    """Test registry.list_manifests"""
    manifests = registry.list_manifests(query=None)
    assert len(manifests) > 0
    assert isinstance(manifests[0], dict)
    logger.info(f"Found {len(manifests)} manifests:")
    logger.info(pf(manifests))

def test_list_manifests_additional_dir(manifest_dict, tmp_path):
    """Test registry.list_manifests with additional directory"""
    new_manifest_path = tmp_path / "new_manifest.yaml"
    manifest_dict["id"] = "my_new_manifest"
    with open(new_manifest_path, "w") as f:
        safe_dump(manifest_dict, f)

    manifests = registry.list_manifests(query=None, additional_dirs=[tmp_path])
    assert len(manifests) > 0
    mani_names = [mani._meta["name"] for mani in manifests]
    mani_ids = [mani._meta["id"] for mani in manifests]
    assert "new_manifest" in mani_names
    assert "my_new_manifest" in mani_ids