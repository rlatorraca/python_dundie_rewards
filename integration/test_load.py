import pytest
from click.testing import CliRunner

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Test command load into terminal"""
<<<<<<< Updated upstream
    out = cmd.invoke(load, PEOPLE_FILE)
    assert "Dunder Mifflin Associates" in out.output
||||||| constructed merge base
    output = check_output(["dundie", "load", PEOPLE_FILE]).decode("utf-8")

    assert "Dundie Mifflin Reward - Associates" in output
=======
    out = cmd.invoke(load, PEOPLE_FILE)
    assert 'Dundie Mifflin Reward - Associates' in out.output
>>>>>>> Stashed changes


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize(
    "wrong_command",
    ["loady", "open", "read", "fetch", "retrieve", "access", "ingest", "initialize", "unpack"]
)
def test_load_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Test command load into terminal"""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output
