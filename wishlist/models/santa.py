from pathlib import Path
from pydantic import BaseModel

from typing import Self
import yaml

from .person import Person
from .relationships import Relationship


class SecretSantaConfig(BaseModel):
    people: list[Person]
    relationships: list[Relationship]

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return cls.model_validate(data)
