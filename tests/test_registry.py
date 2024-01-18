import os
import pytest
from pathlib import Path
from pprint import pformat as pf
from yaml import safe_dump
from datajoint_file_validator import registry, Manifest
from datajoint_file_validator.yaml import is_reference
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


def test_find_from_site_pkg_reference():
    """
    Reference in the manifest directory should resolve correctly.
    """
    ref = registry.find_manifest("demo_rnaseq")
    referenced = registry.find_manifest("demo_rnaseq_v0.1.yaml")
    assert is_reference(ref)
    assert is_reference(str(ref)), "covers casting"
    assert not is_reference(referenced)
    assert Manifest.from_yaml(ref) == Manifest.from_yaml(referenced)

def test_find_in_subdir_from_site_pkg_reference():
    """
    Reference in a subdir within the manifest directory should resolve correctly.
    """
    ref = registry.find_manifest("demo_dlc")
    referenced = registry.find_manifest("demo_dlc/v0.1.yaml")
    assert is_reference(ref)
    assert not is_reference(referenced)
    assert Manifest.from_yaml(ref) == Manifest.from_yaml(referenced)
    with pytest.raises(FileNotFoundError):
        resolved = registry.find_manifest("demo_dlc.yaml")

def test_list_manifests_basic():
    """Test registry.list_manifests"""
    manifests = registry.list_manifests()
    assert len(manifests) > 0
    assert isinstance(manifests[0], dict)
    for mani in manifests:
        assert "id" in mani
        assert "version" in mani
        assert "_meta" in mani

    # Test the query kwarg
    filtered_manis = registry.list_manifests(query="demo")
    mani_names = [mani["_meta"]["stem"] for mani in filtered_manis]
    for mani_name in mani_names:
        assert "demo" in mani_name or "default" in mani_name

    assert not registry.list_manifests(query="gibberish_manifest_name")
    assert registry.list_manifests(query="(gibberish_manifest_name|demo)")


def test_list_manifests_additional_dir(manifest_dict, tmp_path):
    """Test registry.list_manifests with additional directory"""
    new_manifest_path = tmp_path / "new_manifest.yaml"
    manifest_dict["id"] = "my_new_manifest"
    with open(new_manifest_path, "w") as f:
        safe_dump(manifest_dict, f)

    manifests = registry.list_manifests(query=None, additional_dirs=[tmp_path])
    assert len(manifests) > 0
    mani_names = [mani["_meta"]["stem"] for mani in manifests]
    mani_ids = [mani["id"] for mani in manifests]
    assert "new_manifest" in mani_names
    assert "my_new_manifest" in mani_ids


def test_list_manifests_skips_unparseable(manifest_dict, tmp_path):
    """Test registry.list_manifests with yaml file that is not a valid manifest"""
    new_manifest_path = tmp_path / "new_manifest.yaml"
    manifest_dict["id"] = "my_new_manifest"
    manifest_dict["foobar"] = "baz"
    with open(new_manifest_path, "w") as f:
        safe_dump(manifest_dict, f)

    manifests = registry.list_manifests(query=None, additional_dirs=[tmp_path])
    assert len(manifests) > 0
    mani_names = [mani["_meta"]["stem"] for mani in manifests]
    mani_ids = [mani["id"] for mani in manifests]
    assert "new_manifest" not in mani_names
    assert "my_new_manifest" not in mani_ids


def test_list_manifests_sort_alpha():
    """Test registry.list_manifests kwarg sort_alpha"""
    manis_asc = registry.list_manifests(query=None, sort_alpha="asc")
    manis_desc = registry.list_manifests(query=None, sort_alpha="desc")
    assert len(manis_asc) > 1
    assert len(manis_desc) > 1
    assert manis_asc[0]["id"] < manis_asc[-1]["id"]
    assert manis_desc[0]["id"] > manis_desc[-1]["id"]
    assert manis_asc[0] == manis_desc[-1]
    assert manis_asc[-1] == manis_desc[0]

    with pytest.raises(ValueError):
        registry.list_manifests(query=None, sort_alpha="gibberish")


def test_table_from_manifest_list():
    """Test registry.table_from_manifest_list"""
    manifests = registry.list_manifests()
    table = registry.table_from_manifest_list(manifests)
