from pathlib import Path

from wishlist.models import SecretSantaConfig, SecretSantaEvent, SecretSantaPolicy
from wishlist.settings import AppSettings


def main():
    settings = AppSettings()
    santa_list = SecretSantaConfig.from_yaml(Path(settings.config_path))
    policy = SecretSantaPolicy.from_yaml_str(settings.policy_config_path)
    print(santa_list.people)
    print(santa_list.relationships)
    print(policy)

    event = SecretSantaEvent(
        config=santa_list,
        policy=policy
    )

    print(event.generate_assignments())


if __name__ == "__main__":
    main()
