import pytest
import datajoint_file_validator as djfval


@pytest.mark.parametrize(
    "snapshot,expected",
    (
        (
            {
                # foo
            },
            [],
        ),
    ),
)
def test_find_matching_filepaths(snapshot, expected):
    snapshot = {
        # foo
    }
    djfval.query.find_matching_filepaths(snapshot, "foo")