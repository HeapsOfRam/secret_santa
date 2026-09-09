from enum import Enum

from pydantic import BaseModel

from .person import Person


class RelationshipType(str, Enum):
    SPOUSE = "spouse"
    DATING = "dating"
    SIBLING = "sibling"
    PARENT = "parent"
    HOUSEHOLD = "household"
    OTHER = "other"


class Direction(str, Enum):
    BIDIRECTIONAL = "bidirectional"
    UNIDIRECTIONAL = "unidirectional"


class RelationshipGroup(BaseModel):
    people: list[str]
    role: str | None = None


class Relationship(BaseModel):
    type: RelationshipType
    direction: Direction = Direction.BIDIRECTIONAL
    groups: list[RelationshipGroup]

    def contains(self, person: Person) -> bool:
        return any(
            person.id in group.people
            for group in self.groups
        )

    def contains_both(self, person_a, person_b) -> bool:
        return self.contains(person_a) and self.contains(person_b)
