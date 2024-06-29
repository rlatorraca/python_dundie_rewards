import pytest

MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High priority
medium: Medium priority
low: Low priority
win: Run into Windows
"""

# Marker settings
def pytest_configure(config):
    map(lambda line: config.addinivalue_line('markers', line), MARKER.split("\n"))

# Create temporary directories for tests
# ==> Global Settings
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue('tmpdir')
    with tmpdir.as_cwd():
        yield # Build a GENERATORS protocol
