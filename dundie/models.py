# from abc import ABC
# from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional
from pydantic import condecimal, validators
from sqlmodel import Relationship, SQLModel, Field
from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_random_simple_password



class InvalidEmailError(Exception):
    ...


# @dataclass
# class Person(Serializable):
class Person(SQLModel,  table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(nullable=False, index=True)
    name: str = Field(nullable=False)
    dept: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)

    balance: "Balance" = Relationship(back_populates="person")
    movement: "Movement" = Relationship(back_populates="person")
    user: "User" = Relationship(back_populates="person")


    @validators("pk")
    def validate_email(cls, v):
        if not check_valid_email(v):
            raise InvalidEmailError(f"Invalid email address for {v!r}")
        return v

    def __str__(self):
        return f"{self.name} -  {self.dept} -  {self.role}"


# @dataclass
# class Balance(Serializable):
class Balance(SQLModel,  table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person_id")
    person: Person
    value: Annotated[Decimal, Field(default=0, decimal_places=3)]
    person: Person = Relationship(back_populates="balance")
    '''
    def dict(self):
        return {
            "person": self.pk,
            "balance": str(self.value)
        }

    @field_validator("value", mode="before")
    def double_value(cls, v):
        return Decimal(v) * 2
    '''

    class Config:
        json_encoders = {Person: lambda p: p.pk}



# @dataclass
# class Movement(Serializable):
class Movement(SQLModel,  table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person_id")
    date: datetime = Field(default_factory=lambda: datetime.now())
    actor: str
    value: Annotated[Decimal, Field(default=0, decimal_places=3)]

    person: Person = Relationship(back_populates="movement")
    class Config:
        json_encoders = {Person: lambda p: p.pk}


class User(SQLModel,  table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person_id")
    person: Person
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
