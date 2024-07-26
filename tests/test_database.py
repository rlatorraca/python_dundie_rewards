import pytest
from sqlmodel import Session, select

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person
from dundie.utils.db import add_movement, add_person



@pytest.mark.unit
@pytest.mark.high
def test_ensure_database_is_test():
    session = get_session()
    assert "test.db" in session.get_bind().engine.url.database


@pytest.mark.unit
@pytest.mark.high
def test_commit_to_database():
    session = get_session()
    data = {
        "name": "Joe Doe",
        "role": "Salesman",
        "dept": "Sales",
        "email": "joe@doe.com",
    }
    session.add(Person(**data))
    session.commit()

    assert session.exec(select(Person).where(Person.email == data["email"])).first().email == data["email"]


@pytest.mark.unit
@pytest.mark.high
def test_add_person_for_the_first_time():
    data = {
        "role": "Salesman",
        "dept": "Sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    session = get_session()
    person, created = add_person(session, Person(**data))
    assert created is True
    session.commit()
    session.refresh(person)

    assert person.email == data["email"]
    assert person.balance.value == 500
    assert len(person.movement) > 0
    assert person.movement[0].value == 500


@pytest.mark.unit
@pytest.mark.high
def test_negative_add_person_invalid_email():
    """
    with pytest.raises(ValueError):
        add_person({}, ".@bla", {})
    """

    with pytest.raises(InvalidEmailError):
        add_person(Session, Person(email=".@bla"))
        # add_person(mock_session, person_instance)


@pytest.mark.unit
@pytest.mark.high
def test_add_or_remove_points_for_person():
    data = {
        "role": "Salesman",
        "dept": "Sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    session = get_session()
    person, created = add_person(session, Person(**data))
    assert created is True
    session.commit()

    session.refresh(person)
    before = person.balance.value

    add_movement(session, person, -100, "manager")
    session.commit()

    session.refresh(person)
    after = person.balance.value

    assert after == before - 100
    assert after == 400
    assert before == 500
