import pytest
import glob
import datajoint_file_validator as djfval


@pytest.mark.parametrize(
    "manifest_path",
    ("datajoint_file_validator/manifests/demo_dlc_v0.1.yaml",),
)
def test_parse_manifest_from_yaml(manifest_path):
    assert isinstance(manifest_path, str)
    mani = djfval.manifest.Manifest.from_yaml(manifest_path)
    assert isinstance(mani, djfval.manifest.Manifest)


def test_validate_fileset0():
    success, report = djfval.validate(
        "tests/data/filesets/fileset0",
        "datajoint_file_validator/manifests/demo_dlc_v0.1.yaml",
        verbose=True,
        raise_err=False,
    )
    failed_constraints = [item["constraint_id"] for item in report]
    assert not success
    assert isinstance(report, list)
    assert failed_constraints == ["count_min"]


def test_validate_fileset1():
    manifest = djfval.Manifest.from_dict(
        {
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
    )
    success, report = djfval.validate(
        "tests/data/filesets/fileset1",
        manifest,
        verbose=True,
        raise_err=False,
    )
    failed_constraints = [item["constraint_id"] for item in report]
    failed_rules = [item["rule"] for item in report]
    assert not success
    assert isinstance(report, list)
    assert "count_max" in failed_constraints
    assert "max_txt_files" not in failed_rules
