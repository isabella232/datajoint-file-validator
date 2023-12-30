import pytest
from typing import Tuple
from itertools import product
import glob
import datajoint_file_validator as djfval


@pytest.mark.parametrize(
    "manifest_path",
    (
        "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
        "datajoint_file_validator/manifests/demo_dlc/default.yaml",  # Symlink
    ),
)
def test_can_parse_manifest_from_yaml(manifest_path):
    assert isinstance(manifest_path, str)
    mani = djfval.manifest.Manifest.from_yaml(manifest_path)
    assert isinstance(mani, djfval.manifest.Manifest)


@pytest.mark.parametrize(
    "manifest_path, fmt",
    product(
        (
            "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
            "datajoint_file_validator/manifests/demo_dlc/default.yaml",  # Symlink
        ),
        (
            "table",
            "yaml",
            "json",
        ),
    ),
)
def test_error_report_output_format(manifest_path, fmt):
    success, report = djfval.validate(
        "tests/data/filesets/fileset0",
        manifest_path,
        format=fmt,
    )
    assert isinstance(report, list)
    assert isinstance(report[0], dict)


class TestE2EValidaiton:
    def _validate(self, path, manifest, **kw) -> Tuple:
        success, report = djfval.validate(path, manifest, **kw)
        failed_constraints = [item["constraint_id"] for item in report]
        failed_rules = [item["rule"] for item in report]
        return success, report, failed_constraints, failed_rules

    def test_fileset0(self):
        success, report, failed_constraints, failed_rules = self._validate(
            "tests/data/filesets/fileset0",
            "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
        )
        assert not success
        assert isinstance(report, list)
        assert failed_constraints == ["count_min"]

    @pytest.mark.parametrize(
        "verbose, format",
        product(
            (True, False),
            (
                "table",
                "yaml",
                "json",
            ),
        ),
    )
    def test_fileset1(self, verbose, format):
        manifest_dict = {
            "id": "test",
            "version": "0.1",
            "description": "Test manifest",
            "rules": [
                {
                    "id": "count_min_max",
                    "description": "Check count min max",
                    "query": "**",
                    "count_min": 20,
                },
                {
                    # id automatically generated from hash of constraints
                    "count_max": 3,
                },
                {
                    "id": "max_txt_files",
                    "query": "*.txt",
                    "count_max": 5,
                },
                {
                    "eval": "def test_custom(snapshot):\n    return False",
                },
            ],
        }
        manifest = djfval.Manifest.from_dict(manifest_dict)
        assert (
            manifest.rules[1].id
            == djfval.Manifest.from_dict(manifest_dict.copy()).rules[1].id
        ), "inconsistent automatic id generation"

        success, report, failed_constraints, failed_rules = self._validate(
            "tests/data/filesets/fileset1", manifest, verbose=verbose, format=format
        )
        assert not success
        assert isinstance(report, list)
        assert "count_max" in failed_constraints
        assert "max_txt_files" not in failed_rules
