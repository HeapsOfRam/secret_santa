import random

from pydantic import BaseModel, Field

from .assignment import Assignment
from .person import Person
from .policy import DrawMode, SecretSantaPolicy
from .relationships import Relationship
from .santa import SecretSantaConfig


class SecretSantaEvent(BaseModel):
    config: SecretSantaConfig
    policy: SecretSantaPolicy
    assignments: list[Assignment] = Field(default_factory=list)

    def relationships_between(self, person_a: Person, person_b: Person) -> list[Relationship]:
        return [
            relationship
            for relationship in self.config.relationships
            if relationship.contains_both(person_a, person_b)
        ]

    def can_draw(self, giver: Person, recipient: Person) -> bool:
        if self.policy.exclude_self and giver.id == recipient.id:
            return False

        if any(
                relationship in self.policy.excuded_relationship_types
                for relationship in self.relationships_between(giver, recipient)
        ):
            return False

        return True

    def valid_givers_for(self, recipient: Person) -> list[Person]:
        return [
            person
            for person in self.config.people
            if self.can_draw(person, recipient)
        ]

    def valid_recipients_for(self, giver: Person) -> list[Person]:
        return [
            person
            for person in self.config.people
            if self.can_draw(giver, person)
        ]

    def recipient_is_assigned(self, recipient: Person) -> bool:
        return any(
            assignment.recipient.id == recipient.id
            for assignment in self.assignments
        )

    def can_assign(self, giver: Person, recipient: Person) -> bool:
        if not self.can_draw(giver, recipient):
            return False

        if self.policy.giver_draw_mode == DrawMode.WITHOUT_REPLACEMENT:
            if any(
                    assignment.recipient.id == recipient.id
                    for assignment in self.assignments
            ):
                return False

        if self.policy.recipient_draw_mode == DrawMode.WITHOUT_REPLACEMENT:
            if any(
                    assignment.giver.id == giver.id
                    for assignment in self.assignments
            ):
                return False

        return True

    def assign(self, giver: Person, recipient: Person) -> Assignment:
        if not self.can_assign(giver, recipient):
            raise ValueError(f"{giver.name} cannot be assigned to {recipient.name}")
        assignment = Assignment(giver=giver, recipient=recipient)
        self.assignments.append(assignment)
        return assignment

    def generate_assignments(self) -> list[Assignment]:
        for recipient in self.config.people:
            potential_givers = self.valid_givers_for(recipient)
            while not (self.recipient_is_assigned(recipient)):
                giver_candidate = random.choice(potential_givers)
                if self.can_assign(giver_candidate, recipient):
                    self.assign(giver_candidate, recipient)

        return self.assignments
