import pytest
import re
import yaml
from copy import deepcopy
from typing import List, Dict, Union
from wcmatch import glob, pathlib
from datajoint_file_validator import Manifest
from datajoint_file_validator.yaml import read_yaml, is_reference
from datajoint_file_validator.error import InvalidManifestError
from datajoint_file_validator.config import config
from . import logger


class TestManifest:
    def test_from_yaml_and_dict(self, manifest_file_from_registry: str):
        """
        Checks that the Manifest.from_yaml and from_dict methods works as expected.
        """
        manifest_dict = read_yaml(manifest_file_from_registry)
        man1 = Manifest.from_dict(manifest_dict)
        assert isinstance(man1.id, str)
        man2 = Manifest.from_yaml(manifest_file_from_registry)
        assert isinstance(man2.id, str)
        assert man1 == man2

    def test_all_registry_manifests_valid(self, manifest_file_from_registry: str):
        """
        Checks that all manifests in the registry are valid.
        """
        mani = Manifest.from_yaml(manifest_file_from_registry, check_valid=True)

    def test_all_registry_manifests_unique_id(self):
        """
        Checks that all manifests in the registry have unique ids.
        """
        mani_paths = set(
            [
                pathlib.Path(path)
                for path in glob.glob(
                    "datajoint_file_validator/manifests/**/*.yaml", flags=glob.GLOBSTAR
                )
            ]
        )
        mani_ids = list()
        for mani_path in mani_paths:
            if is_reference(mani_path):
                logger.debug(f"Manifest at path '{mani_path=}' is a reference")
                # Ignore: we allow many references to other manifests
                continue
            # from_yaml uses read_yaml, which resolves !include tags
            mani = Manifest.from_yaml(mani_path, check_valid=True)
            mani_ids.append((mani.id, mani.version))
        duplicate_ids = [mani_id for mani_id in mani_ids if mani_ids.count(mani_id) > 1]
        assert len(mani_ids) == len(set(mani_ids)), f"Duplicate ids: {duplicate_ids}"

    def test_check_valid(self, manifest_dict, tmp_path):
        """
        Checks the Manifest.check_valid method.
        """
        fp_valid = tmp_path / "manifest_valid.yaml"
        with open(fp_valid, "w") as f:
            yaml.dump(manifest_dict, f)

        # Create an invalid manifest
        fp_invalid = tmp_path / "manifest_invalid.yaml"
        invalid_dict = deepcopy(manifest_dict)
        invalid_dict["rules"][0]["count_min"] = "not a number"
        invalid_dict["rules"][-1]["eval"] = "lambda x: False"
        with open(fp_invalid, "w") as f:
            yaml.dump(invalid_dict, f)

        # Test the valid manifest
        is_valid, errors = Manifest.check_valid(
            manifest_dict, mani_schema=config.manifest_schema
        )
        assert is_valid, errors
        valid_mani = Manifest.from_yaml(fp_valid, check_valid=True)

        # Test the invalid manifest
        is_valid, errors = Manifest.check_valid(
            invalid_dict, mani_schema=config.manifest_schema
        )
        assert not is_valid
        invalid_mani = Manifest.from_yaml(fp_invalid, check_valid=False)
        with pytest.raises(InvalidManifestError):
            Manifest.from_dict(invalid_dict, check_valid=True)
        with pytest.raises(InvalidManifestError):
            Manifest.from_yaml(fp_invalid, check_valid=True)
