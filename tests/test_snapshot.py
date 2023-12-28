import pytest
from pathlib import Path
from pprint import pprint as pp
import datajoint_file_validator as djfval


class TestSnapshot:
    def _get_paths(self, files):
        assert isinstance(files, list)
        for item in files:
            assert isinstance(item, dict)
        paths = [item["path"] for item in files]
        return paths

    @pytest.mark.parametrize(
        "fileset_path",
        ("tests/data/filesets/fileset1", "tests/data/filesets/fileset1/"),
    )
    def test_fileset1(self, fileset_path):
        files = djfval.snapshot.create_snapshot(fileset_path)
        paths = self._get_paths(files)
        assert set(paths) == set(
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

    @pytest.mark.parametrize(
        "fileset_path",
        (
            "tests/data/filesets/fileset2",
            "tests/data/filesets/fileset2/",
        ),
    )
    def test_fileset2(self, fileset_path):
        files = djfval.snapshot.create_snapshot(fileset_path)
        paths = self._get_paths(files)
        assert set(paths) == set(
            [
                # Note that the subdir is included
                "other_refs/",
                # So is the symlink, even though the resolved path is also included
                "other_ref.fasta",
                "other_refs/mouse_ref_genome.fasta",
                "read1.fasta",
                "read1_r.fasta",
                "read2.fasta",
                "read2_r.fasta",
                "read3.fasta",
                "ref_genome.fasta",
            ]
        )
        for file in files:
            if file["path"] in ("other_refs/"):
                assert file["type"] == "directory"
            else:
                assert file["type"] == "file"

    def test_fileset3(self, fileset_path="tests/data/filesets/fileset3.txt"):
        files = djfval.snapshot.create_snapshot(fileset_path)
        paths = self._get_paths(files)
        assert paths == ["fileset3.txt"]
