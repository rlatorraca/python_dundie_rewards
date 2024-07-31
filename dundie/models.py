# from abc import ABC
# from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_random_simple_password


class InvalidEmailError(Exception):
    """Raised when a email address is invalid"""


# @dataclass
# class Person(Serializable):
class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)
    dept: str = Field(nullable=False, index=True)
    currency: str = Field(default="USD", nullable=True)

    balance: Optional["Balance"] = Relationship(back_populates="person")
    movement: List["Movement"] = Relationship(back_populates="person")
    user: Optional["User"] = Relationship(back_populates="person")

    @property
    def superuser(self):
        # TODO: campo, verificacao em uma tabela RBAC
        return self.email.split("@")[0] in ("jasonsmith")

    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        if not check_valid_email(v):
            raise InvalidEmailError(f"Invalid email address for {v!r}")
        return v

    def __str__(self):
        return f"{self.name} -  {self.dept} -  {self.role}"


# @dataclass
# class Balance(Serializable):
class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    # person: Person
    value: Annotated[Decimal, Field(default=0, decimal_places=2)]

    person: Person = Relationship(back_populates="balance")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


# @dataclass
# class Movement(Serializable):
class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    date: datetime = Field(default_factory=lambda: datetime.now())
    actor: str
    value: Annotated[Decimal, Field(default=0, decimal_places=2)]

    person: Person = Relationship(back_populates="movement")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    password: str = Field(default_factory=generate_random_simple_password)

    person: Person = Relationship(back_populates="user")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


if __name__ == "__main__":
    p = Person(pk="bruno@g.com", name="Bruno", dept="Sales", role="NA")
    print(p)
    print(p.model_dump_json())

    b = Balance(person=p, value=100)
    print(b.model_dump_json())

    m = Movement(person=p, date=datetime.now(), actor="sys", value=10)
    print(m.model_dump_json())

    u = User(person=p)
    print(u.model_dump_json())
