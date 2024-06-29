import pytest

MARKER = """\
unit: Mark unit tests
integration: Mark integration tests
high: High priority
medium: Medium priority
low: Low priority
win: Run into Windows
"""

def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line('markers', line)

# Create temporary directories for tests
# ==> Global Settings
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue('tmpdir')
    with tmpdir.as_cwd():
        yield # Build a GENERATORS protocol
