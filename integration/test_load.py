import pytest
from subprocess import check_output # For Running Linux commands
from .constants import PEOPLE_FILE

@pytest.mark.integration
@pytest.mark.medium
def test_load():
    """Test command load into terminal"""
    output = check_output(['dundie', 'load', PEOPLE_FILE]).decode('utf-8').split('\n')

    assert len(output) == 101
