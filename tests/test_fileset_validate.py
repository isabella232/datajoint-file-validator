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
                    "count_max": 200,
                },
                {
                    # "id": "eval1",
                    "count_min": 20,
                    "count_max": 200,
                },
            ]
        }
    )
    success, report = djfval.validate(
        "tests/data/filesets/fileset1",
        manifest,
        verbose=True,
        raise_err=False,
    )
    failed_constraints = [item["constraint_id"] for item in report]
    assert not success
    assert isinstance(report, list)
    assert failed_constraints == ["count_min"]