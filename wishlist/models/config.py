from .person import Person
from .relationships import Relationship
from .yaml import YamlModel


class SecretSantaConfig(YamlModel):
    people: list[Person]
    relationships: list[Relationship]
