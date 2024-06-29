import pytest
from subprocess import check_output, CalledProcessError  # For Running Linux commands
from .constants import PEOPLE_FILE


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Test command load into terminal"""
    output = check_output(['dundie', 'load', PEOPLE_FILE]).decode('utf-8').split('\n')

    assert len(output) == 101


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize('wrong_command', [
    'loady', 'open', 'read', 'fetch', 'retrieve',
    'access', 'ingest', 'initialize', 'unpack'])
def test_load_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Test command load into terminal"""
    with pytest.raises(CalledProcessError) as error:
        check_output(['dundie', wrong_command, PEOPLE_FILE]).decode('utf-8').split('\n')

    assert "status 2" in str(error.getrepr())
