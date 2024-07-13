# from abc import ABC
# from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_random_simple_password
from pydantic import BaseModel, field_validator, Field


class InvalidEmailError(Exception):
    ...


# @dataclass
# class Person(Serializable):
class Person(BaseModel):
    pk: str
    name: str
    dept: str
    role: str

    '''
    def __post_init(self):
        if check_valid_email(self.pk):
                raise InvalidEmailError("Invalid email address for {self} -> {self.pk!r}")
    '''

    @field_validator("pk")
    def validate_email(cls, v):
        if not check_valid_email(v):
            raise InvalidEmailError(f"Invalid email address for {v!r}")
        return v

    def __str__(self):
        return f"{self.name} -  {self.dept} -  {self.role}"

# @dataclass
# class Balance(Serializable):


class Balance(BaseModel):
    person: Person
    value: Decimal

    '''
    def dict(self):
        return {
            "person": self.pk,
            "balance": str(self.value)
        }
    '''
    @field_validator("value", mode="before")
    def double_value(cls, v):
        return Decimal(v) * 2

    class Config:
        json_encoders = {Person: lambda p: p.pk}

# @dataclass
# class Movement(Serializable):


class Movement(BaseModel):
    person: Person
    date: datetime = Field(default_factory=lambda: datatime.now().isoformat())
    actor: str
    value: Decimal

    class Config:
        json_encoders = {Person: lambda p: p.pk}

class User(BaseModel):
    person: Person
    password: str = Field(default_factory=generate_random_simple_password)

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
