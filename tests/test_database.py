import pytest

from dundie.database import EMPTY_DB, connect


@pytest.mark.unit
@pytest.mark.high
def test_database_empty_or_schema_db_exists():
    db = connect()
    assert db.keys() == EMPTY_DB.keys()
