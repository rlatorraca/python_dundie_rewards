from typing import Optional

from sqlmodel import Session, select

from dundie.models import Balance, InvalidEmailError, Movement, Person, User
from dundie.settings import EMAIL_FROM
from dundie.utils.email import check_valid_email, send_email


def add_person(session: Session, instance: Person):
    """Saves person data to database.
    - If exists, update, else create
    - Set initial balance (managers = 100, others = 500)
    - Generate a password if user is new and send_email
    """

    if not check_valid_email(instance.email):  # Assuming a function to validate email
        raise InvalidEmailError("The provided email is invalid.")

    existing = session.exec(
        select(Person).where(Person.email == instance.email)
    ).first()
    created = existing is None
    if created:
        session.add(instance)
        set_initial_balance(session, instance)
        password = set_initial_password(session, instance)
        # TODO: Usar sistema de filas (conteudo extra)
        send_email(
            EMAIL_FROM, instance.email, "Your dundie password", password
        )
        return instance, created
    else:
        existing.dept = instance.dept
        existing.role = instance.role
        session.add(existing)
        return instance, created


def set_initial_password(session: Session, instance: Person):
    """Generated and saves password"""

    '''
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = generate_random_simple_password(12)
    return db["users"][pk]["password"]
    '''
    user = User(person=instance)  # password generated by model
    session.add(user)
    return user.password


def set_initial_balance(session: Session, instance: Person):
    """Add movement and set initial balanace"""

    '''
    value = 100 if person["role"] == "Manager" else 500
    add_movement(db, pk, value)
    '''
    value = 100 if instance.role == "Manager" else 500
    add_movement(session, instance, value)


def add_movement(
    session: Session,
    instance: Person,
    value: int,
    actor: Optional[str] = "system"):

    """Add movement to user account

    Example::
        Old: add_movement(db, "email@test.com, 100, "Email Name")
        New: add_movement(db, Person(...), 100, "me")
    """


    movement = Movement(person=instance, value=value, actor=actor)
    session.add(movement) # add MOVEMENT to session (in Person)

    # Select all movements for this instance of Person
    movements = session.exec(
        select(Movement).where(Movement.person == instance)
    )

    # Sum all movements values for this instance of Person
    total = sum([mov.value for mov in movements])

    # Get current Balance
    existing_balance = session.exec(
        select(Balance).where(Balance.person == instance)
    ).first()

    if existing_balance:
        existing_balance.value = total
        session.add(existing_balance)
    else:
        session.add(Balance(person=instance, value = total))
