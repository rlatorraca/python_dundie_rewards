MARKER = """\
unit : Mark unit tests
integration : Mark integration tests
high: High priority
medium: Medium priority
low: Low priority
win: Run into Windows
"""

def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line('markers', line)
