import pytest
import glob
import datajoint_file_validator as djfval


@pytest.mark.parametrize('manifest_path,fileset_path', (
    ('datajoint_file_validator/manifests/demo_dlc_v0.1.demo_dlc_v0.1.yaml', 'tests/data/filesets/fileset0'),
))
def test_validate_built_in_filesets(manifest_path, fileset_path):
    snapshot = djfval.snapshot(fileset_path)
    result = djfval.validate(snapshot=snapshot, manifest=manifest_path, verbose=True, raise_err=False)
    assert result['status']