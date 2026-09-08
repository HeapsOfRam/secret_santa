from pathlib import Path

from wishlist.settings import AppSettings
from wishlist.models import SecretSantaConfig


def main():
    settings = AppSettings()
    santa_list = SecretSantaConfig.from_yaml(Path(settings.config_path))
    print(santa_list.people)
    print(santa_list.relationships)


if __name__ == "__main__":
    main()