from pydantic import BaseModel

from .person import Person


class Assignment(BaseModel):
    giver: Person
    recipient: Person
