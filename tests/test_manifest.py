import pytest
import yaml
from wcmatch import glob
from datajoint_file_validator import Manifest


class TestManifest:

    @pytest.mark.parametrize("manifest_file",
        glob.glob('datajoint_file_validator/manifests/**/*.yaml', flags=glob.GLOBSTAR)
    )
    def test_from_yaml_and_dict(self, manifest_file: str):
        """
        Checks that the Manifest.from_yaml and from_dict methods works as expected.
        """
        # Load manifest from file
        with open(manifest_file, 'r') as f:
            manifest_dict = yaml.safe_load(f)
        man1 = Manifest.from_dict(manifest_dict)
        man2 = Manifest.from_yaml(manifest_file)
        assert man1 == man2

