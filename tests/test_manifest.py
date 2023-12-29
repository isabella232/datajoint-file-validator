import pytest
import yaml
from datajoint_file_validator import Manifest


class TestManifest:
    def test_from_yaml_and_dict(self, manifest_file_from_registry: str):
        """
        Checks that the Manifest.from_yaml and from_dict methods works as expected.
        """
        with open(manifest_file_from_registry, "r") as f:
            manifest_dict = yaml.safe_load(f)
        man1 = Manifest.from_dict(manifest_dict, check_valid=False)
        man2 = Manifest.from_yaml(manifest_file_from_registry, check_valid=False)
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
