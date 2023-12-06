import pytest
import glob
import datajoint_file_validator as djfval


@pytest.mark.parametrize('manifest_path', glob.glob('datajoint_file_validator/manifests/*.yaml'))
def test_built_in_manifests(manifest_path):
	djfval.validate(snapshot=snapshot, manifest=manifest_path, verbose=True, raise_err=False)