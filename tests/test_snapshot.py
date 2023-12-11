import pytest
from pathlib import Path
from pprint import pprint as pp
import datajoint_file_validator as djfval


def test_snapshot_fileset1():
    fileset_path = "tests/data/filesets/fileset1"
    files = djfval.snapshot.create_snapshot(fileset_path)
    assert isinstance(files, list)
    for item in files:
        assert isinstance(item, dict)
    paths = [item["path"] for item in files]
    assert set(paths) == set(
        [
            "2021-10-02",
            "2021-10-02/subject1_frame1.png",
            "2021-10-02/subject1_frame2.png",
            "2021-10-02/obs.md",
            "2021-10-02/subject1_frame3.png",
            "2021-10-02/subject1_frame7.png",
            "2021-10-02/subject1_frame0.png",
            "2021-10-02/foo",
            "2021-10-02/foo/bar.txt",
            "2021-10-02/subject1_frame4.png",
            "2021-10-02/subject1_frame6.png",
            "2021-10-02/subject1_frame5.png",
            "obs.md",
            "2021-10-01",
            "2021-10-01/subject1_frame1.png",
            "2021-10-01/subject1_frame2.png",
            "2021-10-01/obs.txt",
            "2021-10-01/subject1_frame3.png",
            "2021-10-01/subject1_frame0.png",
            "2021-10-01/subject1_frame4.png",
            "2021-10-01/subject1_frame5.png",
            "README.txt",
        ]
    )
