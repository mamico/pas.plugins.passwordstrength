from pas.plugins.passwordstrength.testing import FUNCTIONAL_TESTING
from pas.plugins.passwordstrength.testing import INTEGRATION_TESTING
from pas.plugins.passwordstrength.testing import RESTAPI_TESTING
from pathlib import Path
from pytest_plone import fixtures_factory
from requests.exceptions import ConnectionError

import pytest
import requests


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (INTEGRATION_TESTING, "integration"),
            (FUNCTIONAL_TESTING, "functional"),
            (RESTAPI_TESTING, "restapi"),
        )
    )
)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Fixture pointing to the docker-compose file to be used."""
    return Path(str(pytestconfig.rootdir)).resolve() / "tests" / "docker-compose.yml"


def is_responsive(url: str) -> bool:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture
def wait_for():
    def func(thread):
        if not thread:
            return
        thread.join()

    return func
