import importlib
import json
from collections import UserList, defaultdict
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from pydantic import BaseModel

from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import send_email

EMPTY_DB: Dict[str, Dict[str, Any]] = {
    "people": {},
    "balance": {},
    "movement": {},
    "users": {},
}


DB = Dict["BaseModel", "ResultList"]


class ORM:
    """Mapeamento entre "table" no JSON e classes em models"""

    MAPPING = {
        "people": "dundie.models.Person",
        "balance": "dundie.models.Balance",
        "movement": "dundie.models.Movement",
        "users": "dundie.models.User",
    }

    @classmethod
    def get_model_class(cls, table_name):
        module, obj = cls.MAPPING[table_name].rsplit(".", 1)
        return getattr(importlib.import_module(module), obj)

    @classmethod
    def get_table_name(cls, model):
        inverted_orm = {v.split(".")[-1]: k for k, v in cls.MAPPING.items()}
        return inverted_orm[model.__name__]


class NotFoundError(Exception):
    ...


class ResultList(UserList):
    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    def get_by_pk(self, pk):
        print(self[0])
        if len(self) == 0:
            raise NotFoundError(f"{pk} not found")
        try:
            if hasattr(self[0], "pk"):
                return ResultList(
                    item for item in self if item.pk == pk
                ).first()
            return ResultList(
                item for item in self if item.person.pk == pk
            ).first()
        except KeyError:
            raise NotFoundError(f"{pk} not found")

    def filter(self, **query) -> "ResultList":
        if not query:
            return self
        return_data = ResultList()
        for item in self:
            add_item = []
            for q, v in query.items():
                if "__" in q:
                    sub_model, sub_field = q.split("__")
                    related = getattr(item, sub_model)
                    if getattr(related, sub_field) == v:
                        add_item.append(True)
                else:
                    if getattr(item, q) == v:
                        add_item.append(True)
                    else:
                        add_item.append(False)
            if add_item and all(add_item):
                return_data.append(item)
        return return_data


def connect() -> dict:
    """Connect to the database, returning a dict data"""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            # return json.loads(database_file.read())
            raw_data = json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        # return EMPTY_DB
        raw_data = EMPTY_DB
        # transform raw data from json to model objects / Deserialize
    results: Dict[Any, ResultList] = defaultdict(ResultList)
    indexes = {}
    for table_name, data in raw_data.items():
        Model = ORM.get_model_class(table_name)
        results[Model]  # initialize default dict
        if table_name == "people":
            for pk, person_data in data.items():
                instance = Model(pk=pk, **person_data)
                indexes[pk] = instance
                results[Model].append(instance)
        elif table_name == "balance":
            for pk, balance_data in data.items():
                instance = Model(person=indexes[pk], value=balance_data)
                results[Model].append(instance)
        elif table_name == "users":
            for pk, user_data in data.items():
                instance = Model(person=indexes[pk], **user_data)
                results[Model].append(instance)
        elif table_name == "movement":
            for pk, movements in data.items():
                for movement in movements:
                    instance = Model(person=indexes[pk], **movement)
                    results[Model].append(instance)
    return results


def commit(db):
    """Save database in database Json"""
    '''
    if db.keys() != EMPTY_DB.keys():
        print ("Database Schema is invalid: %s" % EMPTY_DB.keys())
        raise RuntimeError("Database Schema is invalid: %s" % db.keys())
    '''

    # transform model objects back to json database / Serialize

    raw_db = defaultdict(dict)
    for model, instances in db.items():
        table_name = ORM.get_table_name(model)
        raw_db[table_name]  # initialize default dict
        for instance in instances:
            raw_instance = json.loads(instance.json())
            if table_name == "people":
                raw_db[table_name][raw_instance.pop("pk")] = raw_instance
            elif table_name == "balance":
                raw_db[table_name][instance.person.pk] = raw_instance["value"]
            elif table_name == "movement":
                table = raw_db[table_name]
                table.setdefault(instance.person.pk, [])
                raw_instance.pop("person")
                table[instance.person.pk].append(raw_instance)
            else:
                raw_instance.pop("person")
                raw_db[table_name][instance.person.pk] = raw_instance

    if raw_db.keys() != EMPTY_DB.keys():
        raise RuntimeError(f"Database Schema is invalid. {raw_db.keys()}")

    final_data = json.dumps(raw_db, indent=4)
    with open(DATABASE_PATH, "w") as database_file:
        # database_file.write(json.dumps(db, indent=4))
        database_file.write(final_data)


def add_person(db, instance):
    # def add_person(db, pk, data):
    """Save person into database.

    - Email must be unique (built by dictonary hash table)
    - If users exists, update, else create
    - Set initial balance (managers = 100, others = 500)
    - Generate a password if user is new and send email to users

    """

    '''
    if not check_valid_email(pk):
        raise ValueError(f"{pk} is not a unique value")

    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)  # if NONE = False, otherwise is True
    person.update(data)
    table[pk] = person
    '''
    Person = ORM.get_model_class("people")
    table = db[Person]
    existing = False
    for person in table:
        if person.pk == instance.pk:
            existing = person
            break
    created = existing is False
    if created:

        table.append(instance)
        set_initial_balance(db, instance)
        password = set_initial_password(db, instance)
        send_email(EMAIL_FROM, instance.pk, "Your dundie password has been", password)

        '''
            set_initial_balance(db, pk, person)
            password = set_initial_password(db, pk)
            send_email(EMAIL_FROM, pk, "Your dundie password has been", password)
            # TODO: Encrypt and send only a link, not a password
        return person, created
        '''
    else:
        existing_data = existing.dict()
        new_data = instance.dict()
        existing_data.update(new_data)
        table.remove(existing)
        table.append(Person(**existing_data))

    return instance, created


def set_initial_password(db, person):
    # def set_initial_password(db, pk):
    """Generated and saves password"""

    '''
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = generate_random_simple_password(12)
    return db["users"][pk]["password"]
    '''
    User = ORM.get_model_class("users")
    user = User(person=person)  # password generated by model
    db[User].append(user)
    return user.password


def set_initial_balance(db, person):
    # def set_initial_balance(db, pk, person):
    """Add movement and set initial balanace"""

    '''
    value = 100 if person["role"] == "Manager" else 500
    add_movement(db, pk, value)
    '''
    value = 100 if person.role == "Manager" else 500
    add_movement(db, person, value)


def add_movement(db, person, value, actor="system"):
    # def add_movement(db, pk, value, actor="system"):
    """Add movement to user account

    Example::
        Old: add_movement(db, "email@test.com, 100, "Email Name")
        New: add_movement(db, Person(...), 100, "me")
    """

    '''
    movements = db["movement"].setdefault(pk, [])
    movements.append({"date": datetime.now().isoformat(), "actor": actor, "value": value})
    db["balance"][pk] = sum([item["value"] for item in movements])
    '''
    Movement = ORM.get_model_class("movement")
    db[Movement].append(Movement(person=person, value=value, actor=actor))
    movements = [item for item in db[Movement] if item.person.pk == person.pk]

    Balance = ORM.get_model_class("balance")
    # reset balance table
    db[Balance] = [item for item in db[Balance] if item.person.pk != person.pk]
    db[Balance].append(
        Balance(person=person, value=sum([item.value for item in movements]))
    )
