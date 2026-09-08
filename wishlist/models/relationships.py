from enum import Enum

from pydantic import BaseModel


class RelationshipType(str, Enum):
    SPOUSE = "spouse"
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
