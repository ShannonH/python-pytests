import pytest


def pytest_addoption(parser):
    parser.addoption("--test_server", action="store", default="https://ultra-integ.int.bbpd.io",
                     help="enter an FQDN")


@pytest.fixture
def test_server(request):
    return request.config.getoption("--test_server")
