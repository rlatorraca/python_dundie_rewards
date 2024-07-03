import pytest

from dundie.core import load

from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_total_100_people():
    """Test Dundie/core.load() function"""
    assert len(load(PEOPLE_FILE)) == 100


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_like_Eve():
    """Test Dundie/core.load() function"""
    assert load(PEOPLE_FILE)[0]["name"] == "Eve Thomas"
