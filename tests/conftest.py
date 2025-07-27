import pytest
import requests_mock as rm


@pytest.fixture
def requests_mock():
    with rm.Mocker() as m:
        yield m
