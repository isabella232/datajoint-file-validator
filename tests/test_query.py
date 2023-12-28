import pytest
import datajoint_file_validator as djfval


class TestGlobQuery:
    def _glob_query(self, pattern, ss):
        filtered_snapshot = djfval.query.GlobQuery(pattern).filter(ss)
        return [item["path"] for item in filtered_snapshot]

    def test_glob_query(self):
        fileset_path = "tests/data/filesets/fileset1"
        ss = djfval.snapshot.create_snapshot(fileset_path)
        ss_paths = [item["path"] for item in ss]

        assert set(self._glob_query("**", ss)) == set(ss_paths)
        assert self._glob_query("2021-10-02", ss) == ["2021-10-02"]
        assert set(self._glob_query("2021-10-02/*", ss)) == set(
            [
                "2021-10-02/subject1_frame1.png",
                "2021-10-02/subject1_frame2.png",
                "2021-10-02/obs.md",
                "2021-10-02/subject1_frame3.png",
                "2021-10-02/subject1_frame7.png",
                "2021-10-02/subject1_frame0.png",
                "2021-10-02/foo",
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
                "2021-10-02/foo",
                "2021-10-02/foo/bar.txt",
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
