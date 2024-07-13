from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from dundie.utils.email import check_valid_email


class InvalidEmailError(Exception):
    ...

@dataclass
class Person:
    pk: str
    name: str
    dept: str
    role: str

    def __post_init(self):
        if check_valid_email(self.pk):
                raise InvalidEmailError("Invalid email address for {self} -> {self.pk!r}")

    def __str__(self):
         return f"{self.name} -  {self.dept} -  {self.role}"

@dataclass
class Balance:
    person: Person
    value: Decimal


@dataclass
class Movement:
    person: Person
    date: datetime
    actor: str
    value: Decimal
