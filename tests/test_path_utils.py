import os
import pytest
from datajoint_file_validator.path_utils import find_matching_paths


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

    assert set(find_matching_paths(example0_paths, "**/*.md")) == {
        "obs.md",
        "2021-10-02/obs.md",
    }
    assert not set(find_matching_paths(example0_paths, "./**.md"))
    assert set(find_matching_paths(example0_paths, "**/*.txt")) == {
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
