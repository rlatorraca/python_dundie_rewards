import pytest

from dundie.core import load
from dundie.database import EMPTY_DB, connect

from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_total_100_people(request):
    """Test Dundie/core.load() function"""
    assert len(load(PEOPLE_FILE)) == 100


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_like_Eve(request):
    """Test Dundie/core.load() function"""
    assert load(PEOPLE_FILE)[0]["name"] == "Eve Thomas"


@pytest.mark.unit
def test_db_schema():
    load(PEOPLE_FILE)
    db = connect()
    assert db.keys() == EMPTY_DB.keys()
