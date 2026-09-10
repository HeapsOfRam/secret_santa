from pathlib import Path

from wishlist.models import SecretSantaConfig, SecretSantaEvent, SecretSantaPolicy
from wishlist.settings import settings
from wishlist.view import AssignmentWriter, MermaidFlowRenderer


def main():
    santa_list = SecretSantaConfig.from_yaml(Path(settings.config_path))
    policy = SecretSantaPolicy.from_yaml_str(settings.policy_config_path)
    print(santa_list.people)
    print(santa_list.relationships)
    print(policy)

    event = SecretSantaEvent(
        config=santa_list,
        policy=policy
    )
    assignments = event.generate_assignments()

    print(assignments)

    writer = AssignmentWriter(MermaidFlowRenderer())
    output = writer.write(assignments)
    print(f"wrote assignments to {output}")


if __name__ == "__main__":
    main()
