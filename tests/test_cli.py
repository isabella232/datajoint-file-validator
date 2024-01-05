import pytest
import shutil
from pathlib import Path
from typer.testing import CliRunner
from datajoint_file_validator.cli import app


@pytest.fixture(scope="module")
def runner():
    return CliRunner(mix_stderr=False)


class TestValidate:
    def test_help(self, runner):
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0

    def test_readme_example(self, runner):
        result = runner.invoke(
            app,
            [
                "validate",
                "tests/data/filesets/fileset0",
                "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
            ],
        )
        assert result.exit_code == 1
        assert "failed" in result.stderr

    def test_readme_example_with_symlink(self, runner):
        result = runner.invoke(
            app,
            [
                "validate",
                "tests/data/filesets/fileset0",
                # "demo_dlc",
                "datajoint_file_validator/manifests/demo_dlc/default.yaml",
            ],
        )
        assert result.exit_code == 1
        assert "failed" in result.stderr

    def test_readme_example_with_discovery(self, runner):
        result = runner.invoke(
            app,
            [
                "validate",
                "tests/data/filesets/fileset0",
                "demo_dlc",
            ],
        )
        assert result.exit_code == 1
        assert "failed" in result.stderr

    def test_readme_example_success(self, runner, tmp_path):
        # Copy fileset0 to a temporary directory
        tmp_fileset = tmp_path / "fileset0"
        tmp_fileset.mkdir()
        for path in Path("tests/data/filesets/fileset0").iterdir():
            shutil.copy(path, tmp_fileset)

        # Failed run
        result = runner.invoke(
            app,
            [
                "validate",
                str(tmp_fileset),
                "demo_dlc",
            ],
        )
        assert result.exit_code == 1
        assert "failed" in result.stderr

        # Add two files to fileset
        (tmp_fileset / "file1.txt").touch()
        (tmp_fileset / "file2.txt").touch()

        # Success run
        result = runner.invoke(
            app,
            [
                "validate",
                str(tmp_fileset),
                "demo_dlc",
            ],
        )
        assert result.exit_code == 0
        assert "failed" not in result.stderr

    @pytest.mark.parametrize("fmt", ("table", "yaml", "json"))
    def test_output_format(self, runner, fmt):
        result = runner.invoke(
            app,
            [
                "validate",
                "--format",
                fmt,
                "tests/data/filesets/fileset0",
                "datajoint_file_validator/manifests/demo_dlc/v0.1.yaml",
            ],
        )
        if fmt == "table":
            assert "━" in result.stdout
        elif fmt == "yaml":
            assert "constraint_id: count_min" in result.stdout
        elif fmt == "json":
            assert "'constraint_id': 'count_min'" in result.stdout

    def test_list_manifests_basic(self, runner):
        result = runner.invoke(
            app,
            [
                "list-manifests",
            ],
        )
        assert result.exit_code == 0
        assert "demo_dlc" in result.stdout

    @pytest.mark.parametrize("fmt", ("table", "yaml", "json"))
    def test_list_manifests_format(self, runner, fmt):
        result = runner.invoke(
            app,
            [
                "list-manifests",
                "--format",
                fmt,
            ],
        )
        assert result.exit_code == 0
        assert "demo_dlc" in result.stdout

        if fmt == "table":
            assert "━" in result.stdout
        elif fmt == "yaml":
            assert "stem: v0.1" in result.stdout
        elif fmt == "json":
            assert "'stem': 'v0.1'" in result.stdout
