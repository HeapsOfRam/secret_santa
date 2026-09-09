import pytest

from wishlist.models import (
    Assignment,
    Person,
    SecretSantaConfig,
    SecretSantaEvent,
    SecretSantaPolicy,
)
from wishlist.models.event import AssignmentAttemptFailed
from wishlist.models.policy import DrawMode
from wishlist.models.relationships import Relationship, RelationshipGroup, RelationshipType


def person(person_id: str) -> Person:
    return Person(id=person_id, name=person_id.title())


def spouse_relationship(person_a: Person, person_b: Person) -> Relationship:
    return Relationship(
        type=RelationshipType.SPOUSE,
        groups=[RelationshipGroup(people=[person_a.id]), RelationshipGroup(people=[person_b.id])],
    )


def test_generate_assignments_returns_a_valid_one_to_one_draw() -> None:
    people = [person(person_id) for person_id in ("alice", "bob", "cora", "dave")]
    event = SecretSantaEvent(
        config=SecretSantaConfig(
            people=people,
            relationships=[spouse_relationship(people[0], people[1])],
        ),
        policy=SecretSantaPolicy(excluded_relationship_types={RelationshipType.SPOUSE}),
    )

    assignments = event.generate_assignments()

    assert len(assignments) == len(people)
    assert {assignment.giver.id for assignment in assignments} == {person.id for person in people}
    assert {assignment.recipient.id for assignment in assignments} == {
        person.id for person in people
    }
    assert all(assignment.giver.id != assignment.recipient.id for assignment in assignments)
    assert all(
        {assignment.giver.id, assignment.recipient.id} != {"alice", "bob"}
        for assignment in assignments
    )


def test_attempt_generate_assignments_rejects_an_impossible_draw() -> None:
    alice, bob = person("alice"), person("bob")
    event = SecretSantaEvent(
        config=SecretSantaConfig(
            people=[alice, bob], relationships=[spouse_relationship(alice, bob)]
        ),
        policy=SecretSantaPolicy(excluded_relationship_types={RelationshipType.SPOUSE}),
    )

    with pytest.raises(AssignmentAttemptFailed):
        event._attempt_generate_assignments()

    assert event.assignments == []


def test_generate_assignments_rejects_existing_assignments() -> None:
    alice, bob = person("alice"), person("bob")
    event = SecretSantaEvent(
        config=SecretSantaConfig(people=[alice, bob], relationships=[]),
        policy=SecretSantaPolicy(),
        assignments=[Assignment(giver=alice, recipient=bob)],
    )

    with pytest.raises(ValueError, match="already has assignments"):
        event.generate_assignments()


def test_generate_assignments_rejects_unsupported_draw_modes() -> None:
    people = [person("alice"), person("bob")]
    event = SecretSantaEvent(
        config=SecretSantaConfig(people=people, relationships=[]),
        policy=SecretSantaPolicy(giver_draw_mode=DrawMode.WITH_REPLACEMENT),
    )

    with pytest.raises(ValueError, match="Only without_replacement"):
        event.generate_assignments()


def test_can_assign_limits_each_giver_and_recipient_without_replacement() -> None:
    alice, bob, cora = (person("alice"), person("bob"), person("cora"))
    event = SecretSantaEvent(
        config=SecretSantaConfig(people=[alice, bob, cora], relationships=[]),
        policy=SecretSantaPolicy(),
    )
    event.assign(alice, bob)

    assert not event.can_assign(alice, cora)
    assert not event.can_assign(cora, bob)
