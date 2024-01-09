import pytest
import datajoint_file_validator as djfval


class TestGlobQuery:
    def _glob_query(self, pattern, ss):
        filtered_snapshot = djfval.query.GlobQuery(pattern).filter(ss)
        return [item["path"] for item in filtered_snapshot]

    def test_glob_query_fileset1(self):
        fileset_path = "tests/data/filesets/fileset1"
        ss = djfval.snapshot.create_snapshot(fileset_path)
        ss_paths = [item["path"] for item in ss]

        assert set(self._glob_query("**", ss)) == set(ss_paths)
        assert self._glob_query("2021-10-02", ss) == ["2021-10-02/"]
        assert set(self._glob_query("2021-10-02/*", ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                "2021-10-02/foo/",
                "2021-10-02/subject1_frame4.png",
                "2021-10-02/subject1_frame6.png",
                "2021-10-02/subject1_frame5.png",
            ]
        )
        assert set(self._glob_query("2021-10-02/**", ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                "2021-10-02/",
                "2021-10-02/foo/",
                "2021-10-02/foo/bar.txt",
                "2021-10-02/subject1_frame4.png",
                "2021-10-02/subject1_frame6.png",
                "2021-10-02/subject1_frame5.png",
            ]
        )
        assert set(self._glob_query("2021-10-02/*", ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                # Note that this now excludes "2021-10-02/"
                "2021-10-02/foo/",
                # Note that this now excludes "2021-10-02/foo/bar.txt"
                "2021-10-02/subject1_frame4.png",
                "2021-10-02/subject1_frame6.png",
                "2021-10-02/subject1_frame5.png",
            ]
        )
        assert set(self._glob_query("**/*.txt", ss)) == set(
            ["2021-10-02/foo/bar.txt", "2021-10-01/obs.txt", "README.txt"]
        )
        assert set(self._glob_query("*.txt", ss)) == set(["README.txt"])
        assert set(self._glob_query("*/**/*.txt", ss)) == set(
            ["2021-10-02/foo/bar.txt", "2021-10-01/obs.txt"]
        )
        assert set(self._glob_query("*/*.txt", ss)) == set(["2021-10-01/obs.txt"])

    def test_glob_query_fileset2(self):
        fileset_path = "tests/data/filesets/fileset2"
        ss = djfval.snapshot.create_snapshot(fileset_path)
        ss_paths = [item["path"] for item in ss]

        assert (
            set(self._glob_query("**", ss))
            == set(ss_paths)
            == set(
                [
                    "ref_genome.fasta",
                    "read2.fasta",
                    "read2_r.fasta",
                    "read1.fasta",
                    "other_ref.fasta",
                    "other_refs/",
                    "other_refs/mouse_ref_genome.fasta",
                    "read3.fasta",
                    "read1_r.fasta",
                ]
            )
        )
        assert not set(self._glob_query("nonexistent", ss))
        assert set(self._glob_query("other_refs/*", ss)) == set(
            ["other_refs/mouse_ref_genome.fasta"]
        )
        assert set(self._glob_query("*/*", ss)) == set(
            ["other_refs/mouse_ref_genome.fasta"]
        )
        assert set(self._glob_query("*/", ss)) == set(["other_refs/"])
        assert set(self._glob_query("*", ss)) == set(
            [
                "ref_genome.fasta",
                "read2.fasta",
                "read2_r.fasta",
                "read1.fasta",
                "other_ref.fasta",
                "other_refs/",
                "read3.fasta",
                "read1_r.fasta",
            ]
        )
        assert set(self._glob_query("*.fasta", ss)) == set(
            [
                "other_ref.fasta",
                "read1.fasta",
                "read1_r.fasta",
                "read2.fasta",
                "read2_r.fasta",
                "read3.fasta",
                "ref_genome.fasta",
            ]
        )
        assert set(self._glob_query("**/*.fasta", ss)) == set(
            [
                "other_ref.fasta",
                "read1.fasta",
                "read1_r.fasta",
                "read2.fasta",
                "read2_r.fasta",
                "read3.fasta",
                "ref_genome.fasta",
                "other_refs/mouse_ref_genome.fasta",
            ]
        )


class TestCompositeQuery:
    def _comp_query(self, pattern, file_type, ss):
        filtered_snapshot = djfval.query.CompositeQuery(
            parts=[
                djfval.query.GlobQuery(pattern),
                djfval.query.TypeQuery(file_type),
            ]
        ).filter(ss)
        return [item["path"] for item in filtered_snapshot]

    def test_from_dict(self):
        query = djfval.query.CompositeQuery.from_dict(
            {
                "path": "2021-10-02/*",
                "type": "file",
            }
        )
        for part in query.parts:
            assert isinstance(part, djfval.query.Query)
        assert query.parts[0].path == "2021-10-02/*"
        assert query.parts[1].file_type == "file"

    def test_from_other(self):
        # with pytest.raises(djfval.error.InvalidQueryError):
        #     djfval.query.CompositeQuery.from_dict(None)
        with pytest.raises(djfval.error.InvalidQueryError):
            djfval.query.CompositeQuery.from_dict("my_str")

    def test_from_dict_empty(self):
        with pytest.raises(djfval.error.InvalidQueryError):
            djfval.query.CompositeQuery.from_dict(dict())

    def test_from_and(self):
        gq = djfval.query.GlobQuery("2021-10-02/*")
        tq = djfval.query.TypeQuery("file")
        cq = gq & tq
        assert isinstance(cq, djfval.query.CompositeQuery)
        assert cq.parts[0] == gq
        assert cq.parts[1] == tq

        # With fileset1
        fileset_path = "tests/data/filesets/fileset1"
        ss = djfval.snapshot.create_snapshot(fileset_path)
        assert set(self._comp_query("2021-10-02/*", "file", ss)) == set([
            file["path"] for file in
            gq.filter(tq.filter(ss))
        ])

        # Test bool
        assert bool(gq) is True
        assert bool(tq) is True
        assert bool(djfval.query.CompositeQuery()) is False

    def test_fileset1(self):
        fileset_path = "tests/data/filesets/fileset1"
        ss = djfval.snapshot.create_snapshot(fileset_path)
        ss_paths = [item["path"] for item in ss]
        assert set(self._comp_query("2021-10-02/*", "file", ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                # "2021-10-02/foo/",
                "2021-10-02/subject1_frame4.png",
                "2021-10-02/subject1_frame6.png",
                "2021-10-02/subject1_frame5.png",
            ]
        )

        assert set(self._comp_query("2021-10-02/*", None, ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                # Now included
                "2021-10-02/foo/",
                "2021-10-02/subject1_frame4.png",
                "2021-10-02/subject1_frame6.png",
                "2021-10-02/subject1_frame5.png",
            ]
        )

        assert set(self._comp_query("2021-10-02/*", "directory", ss)) == set(
            ["2021-10-02/foo/",]
        )
