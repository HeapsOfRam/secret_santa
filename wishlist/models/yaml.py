from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel


class YamlModel(BaseModel):
    @classmethod
    def from_yaml_str(cls, path: str) -> Self:
        return cls.from_yaml(
            Path(path)
        )

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        with path.open() as f:
            data = yaml.safe_load(f)

        return cls.model_validate(data)
