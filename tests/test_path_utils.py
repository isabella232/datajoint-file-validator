import os
import pytest
from datajoint_file_validator.path_utils import find_matching_paths


@pytest.fixture
def filename0_snapshot():
    return [
        {
            "path": "tests/data/filesets/fileset0/2021-10-02_poses.csv",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-02_poses.csv",
            "rel_path": "2021-10-02_poses.csv",
            "size": 0,
            "type": "file",
        },
        {
            "path": "tests/data/filesets/fileset0/2021-10-01_poses.csv",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-01_poses.csv",
            "rel_path": "2021-10-01_poses.csv",
            "size": 0,
            "type": "file",
        },
        {
            "path": "tests/data/filesets/fileset0/2021-10-02_raw.mp4",
            "atime_ns": 1701878056368484156,
            "ctime_ns": 1701878056368484156,
            "last_modified": "2023-12-06T09:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "2021-10-02_raw.mp4",
            "rel_path": "2021-10-02_raw.mp4",
            "size": 0,
            "type": "file",
        },
    ]


@pytest.fixture
def filename0_paths(filename0_snapshot):
    return set([os.path.normpath(file["path"]) for file in filename0_snapshot])


@pytest.fixture
def example0_paths():
    """
    flags = (glob.GLOBSTAR | glob.K | glob.X)
    glob.glob('**', flags=flags)
    """
    return set(
        [
            "2021-10-02/",
            "2021-10-02/subject1_frame1.png",
            "2021-10-02/subject1_frame2.png",
            "2021-10-02/obs.md",
            "2021-10-02/subject1_frame3.png",
            "2021-10-02/subject1_frame7.png",
            "2021-10-02/subject1_frame0.png",
            "2021-10-02/foo/",
            "2021-10-02/foo/bar.txt",
            "2021-10-02/subject1_frame4.png",
            "2021-10-02/subject1_frame6.png",
            "2021-10-02/subject1_frame5.png",
            "obs.md",
            "2021-10-01/",
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


def test_example0_paths(example0_paths):
    assert set(find_matching_paths(example0_paths, "**")) == example0_paths
    assert set(find_matching_paths(example0_paths, ["**"])) == example0_paths
    assert not set(find_matching_paths(example0_paths, "./**"))
    assert not set(find_matching_paths(example0_paths, "./*"))

    assert set(find_matching_paths(example0_paths, "**.md")) == {
        "obs.md",
        "2021-10-02/obs.md",
    }
    assert not set(find_matching_paths(example0_paths, "./**.md"))
    assert set(find_matching_paths(example0_paths, "**.txt")) == {
        "2021-10-01/obs.txt",
        "2021-10-02/foo/bar.txt",
        "README.txt",
    }
    assert set(find_matching_paths(example0_paths, "*/*/*.txt")) == {
        "2021-10-02/foo/bar.txt",
    }
    assert set(find_matching_paths(example0_paths, "*/**/*.txt")) == {
        "2021-10-01/obs.txt",
        "2021-10-02/foo/bar.txt",
    }

    assert set(
        find_matching_paths(example0_paths, "2021-10-0*/subject1_frame*.png")
    ) == {
        "2021-10-01/subject1_frame0.png",
        "2021-10-01/subject1_frame1.png",
        "2021-10-01/subject1_frame2.png",
        "2021-10-01/subject1_frame3.png",
        "2021-10-01/subject1_frame4.png",
        "2021-10-01/subject1_frame5.png",
        "2021-10-02/subject1_frame0.png",
        "2021-10-02/subject1_frame1.png",
        "2021-10-02/subject1_frame2.png",
        "2021-10-02/subject1_frame3.png",
        "2021-10-02/subject1_frame4.png",
        "2021-10-02/subject1_frame5.png",
        "2021-10-02/subject1_frame6.png",
        "2021-10-02/subject1_frame7.png",
    }

    assert set(find_matching_paths(example0_paths, "*/")) == {
        "2021-10-01/",
        "2021-10-02/",
    }
