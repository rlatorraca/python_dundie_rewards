import pytest

from dundie.core import read
from dundie.database import add_person, commit, connect
from dundie.models import Person


@pytest.mark.unit
@pytest.mark.high
def test_read_with_query():
    db = connect()

    pk = "josesilva@dundie.com"
    data = {"name": "Jose da Silva", "role": "Salesman", "dept": "Sales"}
    # _, created = add_person(db, pk, data)
    _, created = add_person(db, Person(pk=pk, **data))
    assert created is True

    pk = "jantoniomorgado@dundie.com"
    data = {"name": "Antonio Morgado", "role": "CEO", "dept": "C-Level"}
    # _, created = add_person(db, pk, data)
    _, created = add_person(db, Person(pk=pk, **data))
    assert created is True

    commit(db)

    response = read()
    assert len(response) == 2

    response = read(dept="Sales")
    assert len(response) == 1
    assert response[0]["name"] == "Jose da Silva"

    response = read(email="jantoniomorgado@dundie.com")
    assert len(response) == 1
    assert response[0]["name"] == "Antonio Morgado"
