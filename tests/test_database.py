import pytest

from dundie.database import EMPTY_DB, connect, commit, add_person


@pytest.mark.unit
@pytest.mark.high
def test_database_empty_or_schema_db_exists():
    db = connect()
    assert db.keys() == EMPTY_DB.keys()


@pytest.mark.unit
@pytest.mark.high
def test_commit_to_databases():
    db = connect()
    data = {
                "name": "Jose da Silva",
                "role": "Salesman",
                "dept": "Sales"
            }
    db["people"]["josesilva@dundie.com"] = data
    commit(db)

    db = connect()
    assert db["people"]["josesilva@dundie.com"] == data


@pytest.mark.unit
@pytest.mark.high
def test_add_person_for_the_first_time():
    pk = "josesilva@dundie.com"
    data = {
                "name": "Jose da Silva",
                "role": "Salesman",
                "dept": "Sales"
            }

    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)

    db = connect()
    assert db["people"][pk] == data
    assert db["balance"][pk] == 500
    assert len(db["movement"][pk]) > 0
    assert db["movement"][pk][0]["value"] == 500


@pytest.mark.unit
@pytest.mark.high
def test_negative_add_person_invalid_email():
    with pytest.raises(ValueError):
        add_person({}, ".@bla", {})
