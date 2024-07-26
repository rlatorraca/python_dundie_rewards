""" Core module """

import os
from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person
from dundie.settings import DATEFORMAT
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.log import get_logger

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


def load(filepath):
    """Data loading function to database

    >>> len(load('assets/people.csv'))
    100

    >>> load('assets/people.csv')[0][0:3]
    'Eve'

    """
    try:
        csv_data = reader(open(filepath))
        next(csv_data)  # Jump first line
    except FileNotFoundError as e:
        log.error(f"File not found: {e}")
        raise e
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise e

    people = []
    headers = ["name", "dept", "role", "email", "currency"]
    with get_session() as session:
        for line in csv_data:
            person_data = dict(zip(headers, [item.strip() for item in line]))
            instance = Person(**person_data)
            person, created = add_person(session, instance)
            return_data = person.model_dump()
            # print(f"Return_data Antes: {return_data}")
            people.append(return_data)
            # print(f"Return_data Depois append: {return_data}")
            return_data.pop("id", None)
            # print(f"Return_data Depois pop id: {return_data}")
            return_data["created"] = created
            # print(f"Return_data Depois created id: {return_data}")

        session.commit()

    return people


def read(**query):
    """Read data from db and filters using query
    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    return_data = []

    query_statements = []
    if "dept" in query:
        query_statements.append(Person.dept == query["dept"])
    if "email" in query:
        query_statements.append(Person.email == query["email"])
    sql = select(Person)  # SELECT FROM PERSON
    if query_statements:
        sql = sql.where(*query_statements)  # WHERE ...

    with get_session() as session:
        # getll all currencies ["BRL", "USD", "EUR", "CAD"]
        currencies = session.exec(select(Person.currency).distinct(Person.currency))
        rates = get_rates(currencies)

        results = session.exec(sql)
        for person in results:
            balance_value = person.balance.value if person.balance else None
            last_movement_date = person.movement[-1].date.strftime(DATEFORMAT) if person.movement else None
            total = rates[person.currency].value * person.balance.value
            return_data.append(
                {
                    "email": person.email,
                    "balance": balance_value,
                    "last_movement": last_movement_date,
                    **person.model_dump(exclude={"id"}),
                    **{"value": total},
                }
            )
    return return_data


def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    with get_session() as session:
        user = os.getenv("USER")
        for person in people:
            instance = session.exec(select(Person).where(Person.email == person["email"])).first()
            if instance is not None:
                add_movement(session, instance, value, user)
        session.commit()
