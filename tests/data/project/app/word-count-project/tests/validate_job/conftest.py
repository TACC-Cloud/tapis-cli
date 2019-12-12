import pytest


def pytest_addoption(parser):
    parser.addoption("--job-directory", action="store", default="job_output",
                     help="Directory containing output to evaluate")


@pytest.fixture
def job_directory(request):
    return request.config.getoption("--job-directory")
