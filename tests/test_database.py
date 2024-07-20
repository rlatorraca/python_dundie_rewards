import pytest

# from dundie.database import EMPTY_DB, add_movement, add_person, commit, connect
from dundie.database import (
    EMPTY_DB,
    ORM,
    add_movement,
    add_person,
    commit,
    connect,
)
from dundie.models import Balance, InvalidEmailError, Movement, Person

@pytest.mark.unit
@pytest.mark.high
def test_database_empty_or_schema_db_exists():
    db = connect()
    # assert db.keys() == EMPTY_DB.keys()
    db_keys = {ORM.get_table_name(model) for model in db}
    assert db_keys == EMPTY_DB.keys()


@pytest.mark.unit
@pytest.mark.high
def test_commit_to_databases():
    db = connect()
    pk ="josesilva@dundie.com"
    data = {"name": "Jose da Silva", "role": "Salesman", "dept": "Sales"}
    # db["people"]["josesilva@dundie.com"] = data
    db[Person].append(Person(pk=pk, **data))
    commit(db)

    db = connect()
    print(db.keys())
    # assert db["people"]["josesilva@dundie.com"] == data
    assert db[Person].get_by_pk("josesilva@dundie.com").dict() == {"pk": pk, **data}
    '''
    added_person = db[Person].get_by_pk("josesilva@dundie.com").dict()
    assert added_person.pk == pk
    assert added_person.name == data["name"]
    assert added_person.role == data["role"]
    assert added_person.dept == data["dept"]
    '''

@pytest.mark.unit
@pytest.mark.high
def test_add_person_for_the_first_time():
    pk = "josesilva@dundie.com"
    data = {"name": "Jose da Silva", "role": "Salesman", "dept": "Sales"}

    db = connect()
    # _, created = add_person(db, pk, data)
    _ , created = add_person(db, Person(pk=pk, **data))
    assert created is True
    commit(db)

    db = connect()
    '''
    assert db["people"][pk] == data
    assert db["balance"][pk] == 500
    assert len(db["movement"][pk]) > 0
    assert db["movement"][pk][0]["value"] == 500
    '''
    added_person = db[Person].get_by_pk(pk)
    assert added_person.pk == pk
    assert added_person.name == data["name"]
    assert added_person.role == data["role"]
    assert added_person.dept == data["dept"]
    assert db[Balance].get_by_pk(pk).value == 500
    assert len(db[Movement].filter(person__pk=pk)) > 0
    assert db[Movement].filter(person__pk=pk).first().value == 500

@pytest.mark.unit
@pytest.mark.high
def test_negative_add_person_invalid_email():
    '''
    with pytest.raises(ValueError):
        add_person({}, ".@bla", {})
    '''
    with pytest.raises(InvalidEmailError):
        add_person({}, Person(pk=".@bla"))


@pytest.mark.unit
@pytest.mark.high
def test_add_or_remove_points_for_person():
    pk = "josesilva@dundie.com"
    data = {"name": "Jose da Silva", "role": "Salesman", "dept": "Sales"}

    db = connect()
    # _, created = add_person(db, pk, data)
    person = Person(pk=pk, **data)
    _, created = add_person(db, person)
    assert created is True
    commit(db)

    db = connect()
    # before = db["balance"][pk]
    before = db[Balance].get_by_pk(pk).value

    # add_movement(db, pk, -100, "manager")
    add_movement(db, person, -100, "manager")
    commit(db)

    db = connect()
    # after = db["balance"][pk]
    after = db[Balance].get_by_pk(pk).value


    assert after == before - 100
    assert after == 400
    assert before == 500
