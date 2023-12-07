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


@pytest.mark.parametrize(
    "manifest_path,fileset_path",
    (
        (
            "datajoint_file_validator/manifests/demo_dlc_v0.1.yaml",
            "tests/data/filesets/fileset0",
        ),
    ),
)
def test_validate_snapshot(manifest_path, fileset_path):
    snapshot = djfval.snapshot.create_snapshot(fileset_path)

    # Check snapshot
    assert snapshot

    # Check validation
    result = djfval.validate.validate_snapshot(
        snapshot=snapshot, manifest_path=manifest_path, verbose=True, raise_err=False
    )
    assert result["status"]
