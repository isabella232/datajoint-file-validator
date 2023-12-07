import pytest


@pytest.fixture
def filename0_snapshot():
    return [
        {
            "abs_path": "tests/data/filesets/fileset0/2021-10-02_poses.csv",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-02_poses.csv",
            "path": "2021-10-02_poses.csv",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset0/2021-10-01_poses.csv",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-01_poses.csv",
            "path": "2021-10-01_poses.csv",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset0/2021-10-02_raw.mp4",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-02_raw.mp4",
            "path": "2021-10-02_raw.mp4",
            "size": 0,
            "type": "file",
        },
    ]


@pytest.fixture
def filename0_paths(filename0_snapshot):
    return set([file["path"] for file in filename0_snapshot])

