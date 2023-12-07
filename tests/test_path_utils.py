import pytest
from datajoint_file_validator.path_utils import find_matching_files, find_matching_paths


class TestFindMatchingPaths:

    def test_same_after_star_star(self, filename0_paths):
        paths = filename0_paths
        assert paths == find_matching_paths(paths, "**")

    def test_find_matching_paths(self, filename0_paths):
        paths = filename0_paths
        assert paths == find_matching_paths(paths, "./**")
