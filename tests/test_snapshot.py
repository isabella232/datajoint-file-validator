import pytest
from pathlib import Path
from pprint import pprint as pp
import datajoint_file_validator as djfval


@pytest.mark.parametrize(
    "fileset_path",
    (
        "tests/data/filesets/fileset0",
        "tests/data/filesets/fileset0/2021-10-01_poses.csv",
        "tests/data/filesets/fileset1",
    ),
)
def test_can_snapshot_to_cls(fileset_path):
    files = djfval.snapshot._snapshot_to_cls(fileset_path)
    assert isinstance(files, list)
    for item in files:
        assert isinstance(item, djfval.snapshot.FileMetadata)
    dicts = [item.asdict() for item in files]
