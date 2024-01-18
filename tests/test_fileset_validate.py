import pytest
from typing import Tuple, Dict, Union
from pathlib import PurePath
from itertools import product
import glob
import datajoint_file_validator as djfval


@pytest.fixture
def snapshot_dict():
    """
    A dictionary representation of a snapshot, from fileset1 using the command:
    snapshot = djfval.snapshot.create_snapshot("tests/data/filesets/fileset1")
    """
    return [
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/",
            "atime_ns": 1704400753730043856,
            "ctime_ns": 1702305330407704090,
            "extension": "",
            "last_modified": "2023-12-11T07:35:30.407704+00:00",
            "mtime_ns": 1702305330407704090,
            "name": "2021-10-02",
            "path": "2021-10-02/",
            "rel_path": "2021-10-02/",
            "size": 4096,
            "type": "directory",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame1.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226880911866,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.880912+00:00",
            "mtime_ns": 1701972226880911866,
            "name": "subject1_frame1.png",
            "path": "2021-10-02/subject1_frame1.png",
            "rel_path": "2021-10-02/subject1_frame1.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame2.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226880911866,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.880912+00:00",
            "mtime_ns": 1701972226880911866,
            "name": "subject1_frame2.png",
            "path": "2021-10-02/subject1_frame2.png",
            "rel_path": "2021-10-02/subject1_frame2.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/obs.md",
            "atime_ns": 1704400889609155753,
            "ctime_ns": 1701878056368484156,
            "extension": ".md",
            "last_modified": "2023-12-06T08:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "obs.md",
            "path": "2021-10-02/obs.md",
            "rel_path": "2021-10-02/obs.md",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame3.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226884911703,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.884912+00:00",
            "mtime_ns": 1701972226884911703,
            "name": "subject1_frame3.png",
            "path": "2021-10-02/subject1_frame3.png",
            "rel_path": "2021-10-02/subject1_frame3.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame7.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226896911215,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.896911+00:00",
            "mtime_ns": 1701972226896911215,
            "name": "subject1_frame7.png",
            "path": "2021-10-02/subject1_frame7.png",
            "rel_path": "2021-10-02/subject1_frame7.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame0.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226880911866,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.880912+00:00",
            "mtime_ns": 1701972226880911866,
            "name": "subject1_frame0.png",
            "path": "2021-10-02/subject1_frame0.png",
            "rel_path": "2021-10-02/subject1_frame0.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/foo/",
            "atime_ns": 1704400753734043626,
            "ctime_ns": 1702305330407704090,
            "extension": "",
            "last_modified": "2023-12-11T07:35:30.407704+00:00",
            "mtime_ns": 1702305330407704090,
            "name": "foo",
            "path": "2021-10-02/foo/",
            "rel_path": "2021-10-02/foo/",
            "size": 4096,
            "type": "directory",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/foo/bar.txt",
            "atime_ns": 1704400889937136667,
            "ctime_ns": 1702305330407704090,
            "extension": ".txt",
            "last_modified": "2023-12-11T07:35:30.407704+00:00",
            "mtime_ns": 1702305330407704090,
            "name": "bar.txt",
            "path": "2021-10-02/foo/bar.txt",
            "rel_path": "2021-10-02/foo/bar.txt",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame4.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226888911540,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.888912+00:00",
            "mtime_ns": 1701972226888911540,
            "name": "subject1_frame4.png",
            "path": "2021-10-02/subject1_frame4.png",
            "rel_path": "2021-10-02/subject1_frame4.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame6.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226892911378,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.892911+00:00",
            "mtime_ns": 1701972226892911378,
            "name": "subject1_frame6.png",
            "path": "2021-10-02/subject1_frame6.png",
            "rel_path": "2021-10-02/subject1_frame6.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-02/subject1_frame5.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972226892911378,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:46.892911+00:00",
            "mtime_ns": 1701972226892911378,
            "name": "subject1_frame5.png",
            "path": "2021-10-02/subject1_frame5.png",
            "rel_path": "2021-10-02/subject1_frame5.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/obs.md",
            "atime_ns": 1704400889605155986,
            "ctime_ns": 1702305330407704090,
            "extension": ".md",
            "last_modified": "2023-12-11T07:35:30.407704+00:00",
            "mtime_ns": 1702305330407704090,
            "name": "obs.md",
            "path": "obs.md",
            "rel_path": "obs.md",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/",
            "atime_ns": 1704400753726044084,
            "ctime_ns": 1702305330399702981,
            "extension": "",
            "last_modified": "2023-12-11T07:35:30.399703+00:00",
            "mtime_ns": 1702305330399702981,
            "name": "2021-10-01",
            "path": "2021-10-01/",
            "rel_path": "2021-10-01/",
            "size": 4096,
            "type": "directory",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame1.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239160420040,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.160420+00:00",
            "mtime_ns": 1701972239160420040,
            "name": "subject1_frame1.png",
            "path": "2021-10-01/subject1_frame1.png",
            "rel_path": "2021-10-01/subject1_frame1.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame2.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239164419882,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.164420+00:00",
            "mtime_ns": 1701972239164419882,
            "name": "subject1_frame2.png",
            "path": "2021-10-01/subject1_frame2.png",
            "rel_path": "2021-10-01/subject1_frame2.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/obs.txt",
            "atime_ns": 1704400889889139460,
            "ctime_ns": 1701878056368484156,
            "extension": ".txt",
            "last_modified": "2023-12-06T08:54:16.368484+00:00",
            "mtime_ns": 1701878056368484156,
            "name": "obs.txt",
            "path": "2021-10-01/obs.txt",
            "rel_path": "2021-10-01/obs.txt",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame3.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239164419882,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.164420+00:00",
            "mtime_ns": 1701972239164419882,
            "name": "subject1_frame3.png",
            "path": "2021-10-01/subject1_frame3.png",
            "rel_path": "2021-10-01/subject1_frame3.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame0.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239160420040,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.160420+00:00",
            "mtime_ns": 1701972239160420040,
            "name": "subject1_frame0.png",
            "path": "2021-10-01/subject1_frame0.png",
            "rel_path": "2021-10-01/subject1_frame0.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame4.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239164419882,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.164420+00:00",
            "mtime_ns": 1701972239164419882,
            "name": "subject1_frame4.png",
            "path": "2021-10-01/subject1_frame4.png",
            "rel_path": "2021-10-01/subject1_frame4.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/2021-10-01/subject1_frame5.png",
            "atime_ns": 1704314007822729854,
            "ctime_ns": 1701972239168419724,
            "extension": ".png",
            "last_modified": "2023-12-07T11:03:59.168420+00:00",
            "mtime_ns": 1701972239168419724,
            "name": "subject1_frame5.png",
            "path": "2021-10-01/subject1_frame5.png",
            "rel_path": "2021-10-01/subject1_frame5.png",
            "size": 0,
            "type": "file",
        },
        {
            "abs_path": "tests/data/filesets/fileset1/README.txt",
            "atime_ns": 1704400889889139460,
            "ctime_ns": 1702305330407704090,
            "extension": ".txt",
            "last_modified": "2023-12-11T07:35:30.407704+00:00",
            "mtime_ns": 1702305330407704090,
            "name": "README.txt",
            "path": "README.txt",
            "rel_path": "README.txt",
            "size": 0,
            "type": "file",
        },
    ]


@pytest.mark.parametrize(
    "manifest_path",
    (
        "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
        "datajoint_file_validator/manifests/demo_dlc/default.yaml",  # Symlink
    ),
)
def test_can_parse_manifest_from_yaml(manifest_path):
    assert isinstance(manifest_path, str)
    mani = djfval.manifest.Manifest.from_yaml(manifest_path)
    assert isinstance(mani, djfval.manifest.Manifest)


@pytest.mark.parametrize(
    "manifest_path, fmt",
    product(
        (
            "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
            "datajoint_file_validator/manifests/demo_dlc/default.yaml",  # Symlink
        ),
        (
            "table",
            "yaml",
            "json",
        ),
    ),
)
def test_error_report_output_format(manifest_path, fmt):
    success, report = djfval.validate(
        "tests/data/filesets/fileset0",
        manifest_path,
        format=fmt,
    )
    assert isinstance(report, list)
    assert isinstance(report[0], dict)


class TestE2EValidaiton:
    """These tests perform basic end-to-end checks for fileset validation."""

    def _validate(self, path, manifest, **kw) -> Tuple:
        success, report = djfval.validate(path, manifest, **kw)
        failed_constraints = [item["constraint_id"] for item in report]
        failed_rules = [item["rule"] for item in report]
        return success, report, failed_constraints, failed_rules

    def test_fileset0(self):
        success, report, failed_constraints, failed_rules = self._validate(
            "tests/data/filesets/fileset0",
            "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
        )
        assert not success
        assert isinstance(report, list)
        assert failed_constraints == ["count_min"]

    @pytest.mark.parametrize(
        "verbose, format",
        product(
            (True, False),
            (
                "table",
                "yaml",
                "json",
            ),
        ),
    )
    def test_fileset1(self, verbose, format, manifest_dict):
        manifest = djfval.Manifest.from_dict(manifest_dict)
        assert (
            manifest.rules[1].id
            == djfval.Manifest.from_dict(manifest_dict.copy()).rules[1].id
        ), "inconsistent automatic id generation"

        success, report, failed_constraints, failed_rules = self._validate(
            "tests/data/filesets/fileset1", manifest, verbose=verbose, format=format
        )
        assert not success
        assert isinstance(report, list)
        assert "count_max" in failed_constraints
        assert "max_txt_files" not in failed_rules

    def test_invalid_format(self, manifest_dict):
        """Test invalid format specification"""
        manifest = djfval.Manifest.from_dict(manifest_dict)
        with pytest.raises(ValueError):
            self._validate(
                "tests/data/filesets/fileset1",
                manifest,
                verbose=True,
                format="invalid_format",
            )

    def test_fail_with_raise_err(self, manifest_dict):
        """Test raises on failure if raise_err=True"""
        manifest = djfval.Manifest.from_dict(manifest_dict)
        with pytest.raises(djfval.error.DJFileValidatorError):
            self._validate(
                "tests/data/filesets/fileset1",
                manifest,
                verbose=True,
                format="table",
                raise_err=True,
            )


class TestSnapshotValidation:
    """These tests check manifest dictionaries against the snapshot."""

    def _validate(self, snapshot_dict, manifest_dict, **kw) -> Tuple:
        manifest = djfval.Manifest.from_dict(manifest_dict)
        success, report = djfval.validate(snapshot_dict, manifest, **kw)
        failed_constraints = [item["constraint_id"] for item in report]
        failed_rules = [item["rule"] for item in report]
        return success, report, failed_constraints, failed_rules

    def _new_file(self, path: str, type: str = "file", **kw) -> Dict:
        return dict(
            path=path,
            type=type,
            extension=PurePath(path).suffix if type == "file" else "",
            **kw,
        )

    def test_snapshot(self, snapshot_dict, manifest_dict):
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert not success
        assert isinstance(report, list)
        assert failed_constraints == ["count_max", "eval"]
        assert "max_txt_files" not in failed_rules

    def test_snapshot_max_txt_files_anywhere(self, snapshot_dict, manifest_dict):
        manifest_dict["rules"].append(
            dict(
                id="max_txt_files_anywhere",
                query="**/*.txt",
                count_max=3,
            )
        )
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert not success
        assert isinstance(report, list)
        assert failed_constraints == ["count_max", "eval"]
        assert "max_txt_files_anywhere" not in failed_rules

    def test_snapshot_more_top_level_txt(self, snapshot_dict, manifest_dict):
        for i in range(5):
            snapshot_dict.append(self._new_file(f"new_file_{i}.txt"))
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert not success
        assert "max_txt_files" in failed_rules

    def test_snapshot_more_top_level_txt(self, snapshot_dict, manifest_dict):
        for i in range(5):
            snapshot_dict.append(self._new_file(f"new_file_{i}.txt"))
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert not success
        assert "max_txt_files" in failed_rules

    def test_snapshot_regex_and_eval_updates(self, snapshot_dict, manifest_dict):
        manifest_dict["rules"][-1][
            "eval"
        ] = "def test_custom(snapshot):\n    return True"
        manifest_dict["rules"][1]["query"] = "*.md"
        manifest_dict["rules"][1]["id"] = "max_md_files"
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert success
        assert "max_md_files" not in failed_rules

    def test_snapshot_regex_and_eval_updates_fail(self, snapshot_dict, manifest_dict):
        manifest_dict["rules"][-1]["eval"] = (
            "def test_custom(snapshot):\n    return len([file for file "
            "in snapshot if file['extension'] == '.md']) < 3"
        )
        manifest_dict["rules"][-1]["id"] = "max_md_files_eval"
        manifest_dict["rules"][1]["query"] = "*.md"
        manifest_dict["rules"][1]["id"] = "max_md_files"
        for i in range(3):
            snapshot_dict.append(self._new_file(f"new_file_{i}.md"))
        success, report, failed_constraints, failed_rules = self._validate(
            snapshot_dict, manifest_dict
        )
        assert not success
        assert "max_md_files" in failed_rules
        assert "max_md_files_eval" in failed_rules
