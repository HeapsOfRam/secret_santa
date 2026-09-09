from pydantic_settings import BaseSettings, SettingsConfigDict

from wishlist.constants import app_constants


class AppSettings(BaseSettings):
    config_path: str = app_constants.DEFAULT_CONFIG_PATH
    policy_config_path: str = app_constants.DEFAULT_POLICY_CONFIG_PATH

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
