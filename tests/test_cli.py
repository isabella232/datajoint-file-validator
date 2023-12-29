import pytest
from typer.testing import CliRunner
from datajoint_file_validator.cli import app


@pytest.fixture(scope="module")
def runner():
    return CliRunner(mix_stderr=False)


class TestValidate:
    def test_help(self, runner):
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        # assert "Hello Camila" in result.stdout
        # assert "Let's have a coffee in Berlin" in result.stdout

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
