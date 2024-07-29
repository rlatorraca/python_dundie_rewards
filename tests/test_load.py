import pytest

from dundie.core import load

from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_total_100_people(request):
    """Test Dundie/core.load() function"""
    assert len(load(PEOPLE_FILE)) == 100


@pytest.mark.unit
@pytest.mark.high
def test_load_negative_file_not_found(request):
    """Test Dundie/core.load() function"""
    with pytest.raises(FileNotFoundError):
        assert load("assets/invalid_file.csv")


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_like_Zachary(request):
    """Test Dundie/core.load() function"""
    assert load(PEOPLE_FILE)[0]["name"] == "Zachary Bowman"
