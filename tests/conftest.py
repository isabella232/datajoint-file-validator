import pytest
from typing import Dict
from wcmatch import glob


@pytest.fixture(
    params=glob.glob(
        "datajoint_file_validator/manifests/**/*.yaml", flags=glob.GLOBSTAR
    )
)
def manifest_file_from_registry(request) -> str:
    """Returns path to every manifest file in the registry."""
    return request.param


@pytest.fixture
def manifest_dict() -> Dict:
    """A valid dictionary that can be used to create a manifest."""
    return {
        "id": "test",
        "version": "0.1",
        "description": "Test manifest",
        "rules": [
            {
                "id": "count_min_max",
                "description": "Check count min max",
                "query": "**",
                "count_min": 20,
            },
            {
                # id automatically generated from hash of constraints
                "count_max": 3,
            },
            {
                "id": "max_txt_files",
                "query": "*.txt",
                "count_max": 5,
            },
            {
                "eval": "def test_custom(snapshot):\n    return False",
            },
        ],
    }
