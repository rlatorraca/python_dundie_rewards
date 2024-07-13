from abc import ABC
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from dundie.utils.email import check_valid_email


class InvalidEmailError(Exception):
    ...


class Serializable(ABC):
     def dict(self):
          return vars(self)

@dataclass
class Person(Serializable):
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
class Balance(Serializable):
    person: Person
    value: Decimal

    def dict(self):
         return {
              "person": self.pk,
              "balance": str(self.value)
         }


@dataclass
class Movement(Serializable):
    person: Person
    date: datetime
    actor: str
    value: Decimal
