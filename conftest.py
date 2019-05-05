import pytest
from tests.credentials import credentials


@pytest.fixture()
def current_credentials():
    return credentials
