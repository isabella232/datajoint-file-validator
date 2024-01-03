import pytest
import yaml
from datajoint_file_validator import Manifest
from datajoint_file_validator.yaml import read_yaml


class TestManifest:
    def test_from_yaml_and_dict(self, manifest_file_from_registry: str):
        """
        Checks that the Manifest.from_yaml and from_dict methods works as expected.
        """
        manifest_dict = read_yaml(manifest_file_from_registry)
        man1 = Manifest.from_dict(manifest_dict)
        man2 = Manifest.from_yaml(manifest_file_from_registry)
        assert man1 == man2

    def test_all_registry_manifests_valid(self, manifest_file_from_registry: str):
        """
        Checks that all manifests in the registry are valid.
        """
        mani = Manifest.from_yaml(manifest_file_from_registry, check_valid=True)

    def test_check_valid(self, manifest_file_from_registry: str):
        """
        Checks the Manifest.check_valid method.
        """
        pass

