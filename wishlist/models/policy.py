from enum import StrEnum

from pydantic import Field

from .relationships import RelationshipType
from .yaml import YamlModel


class DrawMode(StrEnum):
    WITH_REPLACEMENT = "with_replacement"
    WITHOUT_REPLACEMENT = "without_replacement"


class SecretSantaPolicy(YamlModel):
    exclude_self: bool = True
    excluded_relationship_types: set[RelationshipType] = Field(
        default_factory=set
    )
    avoid_previous_years: int = 0
    prevent_reciprocal_pairs: bool = False
    giver_draw_mode: DrawMode = DrawMode.WITHOUT_REPLACEMENT
    recipient_draw_mode: DrawMode = DrawMode.WITHOUT_REPLACEMENT
