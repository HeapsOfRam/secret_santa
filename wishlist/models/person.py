from pydantic import BaseModel, Field


class Person(BaseModel):
    id: str
    name: str

    desired_items: list[str] = Field(default_factory=list)
    shirt_size: str | None = None
