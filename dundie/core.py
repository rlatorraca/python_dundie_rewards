""" Core module """

import os
from csv import reader

from dundie.database import add_movement, add_person, commit, connect
from dundie.utils.log import get_logger

log = get_logger()

lines = []


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

    db = connect()
    people = []
    headers = ["name", "dept", "role", "email"]
    for line in csv_data:
        person_data = dict(zip(headers, [item.strip() for item in line]))

        pk = person_data.pop("email")
        person, created = add_person(db, pk, person_data)

        return_data = person.copy()
        return_data["created"] = created
        return_data["email"] = pk
        people.append(return_data)

    commit(db)
    return people


def read(**query):
    """Read data from db and filters using query
    read(email="joe@doe.com")
    """
    db = connect()
    return_data = []
    for pk, data in db["people"].items():

        dept = query.get("dept")
        if dept and dept != data["dept"]:  # Check by DEPT (is in the database)
            continue

        # WALRUS / Assignment Expression - a partir do python 3.8
        if (email := query.get("email")) and email != pk:  # Check by EMAIL (is in the database)
            continue

        return_data.append(
            {
                "email": pk,
                "balance": db["balance"][pk],
                "last_movement": db["movement"][pk][-1]["date"],
                **data,
            }
        )

    return return_data


def add(value, **query):
    """Add value to each record on query"""
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    db = connect()
    user = os.getenv("USER")
    for person in people:
        add_movement(db, person["email"], value, user)
    commit(db)
