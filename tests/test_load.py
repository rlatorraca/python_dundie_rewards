import pytest
import os
import uuid
from dundie.core import load
from .constants import PEOPLE_FILE

def setup_module():
    print("\nRun BEFORE all modules/file tests")

def teardown_module():
    print("\nRun AFTER all modules/file tests")

@pytest.fixture(scope="function", autouse=True) # autouse=True -> used by all functions in this file
def create_new_file(tmpdir): # This tmpdir injected by conftest @pytest.fixture (Global)
    # Run BEFORE all functions(tests) in this file
    file_ = tmpdir.join("AnyFile.txt")
    file_.write("RLSP - Any info")

    yield # Test running on this line

    # Run AFTER all functions(tests) in this file
    file_.remove() # remove file after test done

@pytest.mark.unit
@pytest.mark.high
def test_load(request):
    """Test Dundie/core.load() function"""
    filepath = f"File_not_wanted-(uuid.uuid4()).txt"

    request.addfinalizer(lambda: os.unlink(filepath)) # remove file after test done
    request.addfinalizer(lambda: print("--> Test Done by RLSP"))

    with open(filepath, "w") as file_:
            file_.write("RLSP - All data just used by this test")
    assert len(load(PEOPLE_FILE)) == 100
    assert load(PEOPLE_FILE)[0][0:3] == 'Eve'
