import pytest
from pathlib import Path
from pprint import pprint as pp
import datajoint_file_validator as djfval


@pytest.mark.parametrize(
    "fileset_path",
    (
        "tests/data/filesets/fileset0",
        "tests/data/filesets/fileset0/2021-10-01_poses.csv",
    ),
)
def test_can_snapshot(fileset_path):
    snapshot = djfval.snapshot(fileset_path)
    pp(snapshot)
    # breakpoint()
    assert isinstance(snapshot, list)
    for item in snapshot:
        assert isinstance(item, djfval.FileMetadata)
    dicts = [item.asdict() for item in snapshot]
