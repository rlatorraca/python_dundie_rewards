""" Core module """
from csv import reader
from dundie.utils.log import get_logger
from dundie.database import connect, add_person, add_movement, commit

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
