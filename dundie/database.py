import json

from datetime import datetime
from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import check_valid_email, send_email
from dundie.utils.user import generate_random_simple_password

EMPTY_DB = {"people": {}, "balance": {}, "movement": {}, "users": {}}


def connect() -> dict:
    """Connect to the database, returning a dict data"""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return EMPTY_DB


def commit(db):
    """Save database in database Json"""
    if db.keys() != EMPTY_DB.keys():
        raise RuntimeError("Database Schema is invalid: %s" % db.keys())

    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_person(db, pk, data):
    """Save person into database.

    - Email must be unique (built by dictonary hash table)
    - If users exists, update, else create
    - Set initial balance (managers = 100, others = 500)
    - Generate a password if user is new and send email to users

    """

    if not check_valid_email(pk):
        raise ValueError(f"{pk} is not a unique value")

    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)  # if NONE = False, otherwise is True
    person.update(data)
    table[pk] = person
    if created:
        set_initial_balance(db, pk, person)
        password = set_initial_password(db, pk)
        send_email(EMAIL_FROM, pk, "Your dundie password has been", password)
        # TODO: Encrypt and send only a link, not a password
    return person, created


def set_initial_password(db, pk):
    """Generated and saves password"""
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = generate_random_simple_password(12)
    return db["users"][pk]["password"]


def set_initial_balance(db, pk, person):
    """Add movement and set initial balanace"""
    value = 100 if person["role"] == "Manager" else 500
    add_movement(db, pk, value)


def add_movement(db, pk, value, actor="system"):
    movements = db["movement"].setdefault(pk, [])
    movements.append(
        {
            "date": datetime.now().isoformat(),
            "actor": actor,
            "value": value
        }
    )
    db["balance"][pk] = sum([item["value"] for item in movements])
