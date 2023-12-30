import pytest
from wcmatch import glob


@pytest.fixture(
    params=glob.glob(
        "datajoint_file_validator/manifests/**/*.yaml", flags=glob.GLOBSTAR
    )
)
def manifest_file_from_registry(request) -> str:
    """Returns path to every manifest file in the registry."""
    return request.param
