from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

from wishlist.constants import app_constants
from wishlist.models.person import Person
from wishlist.models.relationships import Relationship


class AppSettings(BaseSettings):
    config_path: str = app_constants.DEFAULT_CONFIG_PATH
    policy_config_path: str = app_constants.DEFAULT_POLICY_CONFIG_PATH

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
