import os
import pytest
from datajoint_file_validator.path_utils import find_matching_files, find_matching_paths


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


class TestFindMatchingPaths:

    def test_same_after_star_star(self, filename0_paths):
        paths = filename0_paths
        assert paths == find_matching_paths(paths, "**")

    def test_so_example(self):
        paths = ['/foo/bar/baz', '/spam/eggs/baz', '/foo/bar/bar']
        assert find_matching_paths(paths, '/foo/bar/*') == set(['/foo/bar/baz', '/foo/bar/bar'])
        assert find_matching_paths(paths, '/*/bar/b*') == set(['/foo/bar/baz', '/foo/bar/bar'])
        assert find_matching_paths(paths, '/*/[be]*/b*') == set(['/foo/bar/baz', '/foo/bar/bar', '/spam/eggs/baz'])
        assert not find_matching_paths(paths, '/*/[xq]*/b*')
        assert find_matching_paths(paths, '/**') == paths
        assert find_matching_paths(paths, '/*/**') == paths
        assert find_matching_paths(paths, '/**/*') == paths
        assert find_matching_paths(paths, '**/*') == paths
        assert find_matching_paths(paths, '**/**') == paths

    def test_find_matching_paths(self, filename0_paths):
        paths = filename0_paths
        assert paths == find_matching_paths(paths, "/**")
