import pytest
from pathlib import Path
from pprint import pprint as pp
import datajoint_file_validator as djfval


@pytest.mark.parametrize('fileset_path, expected', (
    ('tests/data/filesets/fileset0', [
		{
			"": "",
		},
    ]),
    ('tests/data/filesets/fileset0/2021-10-01_poses.csv', [
		{
			"": "",
		},
    ]),
))
def test_can_snapshot(fileset_path, expected):
	snapshot = djfval.snapshot(fileset_path)
	pp(snapshot)
	# breakpoint()
	assert isinstance(snapshot, list)
	for item in snapshot:
		assert isinstance(item, dict)
		for key, value in item.items():
			assert isinstance(key, (str, Path))
			# assert isinstance(value, str)
	assert snapshot == expected

