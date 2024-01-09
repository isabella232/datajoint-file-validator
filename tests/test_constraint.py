import pytest
from datajoint_file_validator.constraint import (
    Constraint,
    EvalConstraint,
    CountMinConstraint,
    RegexConstraint,
)
from datajoint_file_validator.snapshot import create_snapshot, Snapshot
from datajoint_file_validator.error import DJFileValidatorError
from datajoint_file_validator.config import config


@pytest.fixture(scope="module")
def snapshot_fileset1() -> Snapshot:
    return create_snapshot("tests/data/filesets/fileset1")


@pytest.fixture
def disable_feature_allow_eval():
    og_val = config.allow_eval
    config.allow_eval = False
    yield
    config.allow_eval = og_val


class TestCountMinConstraint:
    def test_str_value(self):
        """Check that CountMinConstraint (and dataclasses in general)
        will allow a string value even if the annotation is int."""
        # Valid
        c = CountMinConstraint(2)
        assert c.val == 2

        # Also valid
        c = CountMinConstraint("a string")
        assert c.val == "a string"


class TestRegexConstraint:
    def test_basic_usage_pass(self, snapshot_fileset1: Snapshot):
        c = RegexConstraint(".+")
        assert c.val == ".+"
        result = c.validate(snapshot_fileset1)
        assert result.status is True

    def test_basic_usage_fail(self, snapshot_fileset1: Snapshot):
        failing_patterns = (
            "^.*\\.mp4$|.*\\.csv$",
            "^.*\\.mp4$|.*\\.csv|.*\\.png$",
            "^.+\\.txt$|.+\\.md|.+\\.png$",
            "^.+\\.txt$|.+\\.md|.+\\.png|2021-10-0[12]/$",
        )
        for pattern in failing_patterns:
            c = RegexConstraint(pattern)
            result = c.validate(snapshot_fileset1)
            assert result.status is False

    def test_fileset1_passing(self, snapshot_fileset1: Snapshot):
        passing_patterns = (
            "^.+\\.txt$|.+\\.md|.+\\.png|2021-10-0[12]/(?:foo/)?$",
        )
        for pattern in passing_patterns:
            c = RegexConstraint(pattern)
            result = c.validate(snapshot_fileset1)
            assert result.status is True


class TestEvalConstraint:
    def test_error_if_disabled(
        self, snapshot_fileset1: Snapshot, disable_feature_allow_eval
    ):
        c = EvalConstraint(
            "def func(snapshot: List[Dict[str, Any]]) -> bool: "
            "return len(snapshot) > 0"
        )
        with pytest.raises(DJFileValidatorError):
            c.validate(snapshot_fileset1)

    def test_basic_usage_success(self, snapshot_fileset1: Snapshot):
        c = EvalConstraint(
            "def func(snapshot: List[Dict[str, Any]]) -> bool: "
            "return len(snapshot) > 0"
        )
        result = c.validate(snapshot_fileset1)
        assert result.status is True

    def test_basic_usage_failure(self, snapshot_fileset1: Snapshot):
        c = EvalConstraint(
            "def func(snapshot: List[Dict[str, Any]]) -> bool: " "return False"
        )
        result = c.validate(snapshot_fileset1)
        assert result.status is False
        assert "failed" in result.message

    def test_func_invalid_syntax(self, snapshot_fileset1: Snapshot):
        c = EvalConstraint("def func(snapshot: my_dummy_type) -> bool: " "return True")
        with pytest.raises(Exception):
            c.validate(snapshot_fileset1)

    def test_func_that_raises(self, snapshot_fileset1: Snapshot):
        c = EvalConstraint(
            "def func(snapshot: List[Dict[str, Any]]) -> bool: "
            "raise Exception('foo')"
        )
        with pytest.raises(Exception):
            c.validate(snapshot_fileset1)

    def test_bad_func_name(self, snapshot_fileset1: Snapshot):
        c = EvalConstraint("lambda x: x > 0")
        with pytest.raises(DJFileValidatorError):
            c.validate(snapshot_fileset1)

    def test_syntax_error(self, snapshot_fileset1: Snapshot):
        """Raises error due to trailing parenthesis."""
        c = EvalConstraint(
            "def test_custom(snapshot):\n    return len(file for file in "
            "snapshot if file['extension'] == '.md') < 3)"
        )
        with pytest.raises(DJFileValidatorError) as e:
            c.validate(snapshot_fileset1)
        assert "SyntaxError" in str(e.value)
