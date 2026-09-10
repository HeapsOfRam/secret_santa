import random

from pydantic import BaseModel, Field

from .assignment import Assignment
from .config import SecretSantaConfig
from .person import Person
from .policy import DrawMode, SecretSantaPolicy


class AssignmentAttemptFailed(Exception):
    pass


class SecretSantaEvent(BaseModel):
    config: SecretSantaConfig
    policy: SecretSantaPolicy
    assignments: list[Assignment] = Field(default_factory=list)

    def can_assign(
        self,
        giver: Person,
        recipient: Person,
        assignments: list[Assignment] | None = None,
    ) -> bool:
        assignments = self.assignments if assignments is None else assignments

        if self.policy.exclude_self and giver.id == recipient.id:
            return False

        if any(
            relationship.type in self.policy.excluded_relationship_types
            and relationship.contains_both(giver, recipient)
            for relationship in self.config.relationships
        ):
            return False

        if self.policy.giver_draw_mode == DrawMode.WITHOUT_REPLACEMENT:
            if any(
                assignment.giver.id == giver.id for assignment in assignments
            ):
                return False

        if self.policy.recipient_draw_mode == DrawMode.WITHOUT_REPLACEMENT:
            if any(
                assignment.recipient.id == recipient.id for assignment in assignments
            ):
                return False

        if self.policy.prevent_reciprocal_pairs and any(
            assignment.giver.id == recipient.id and assignment.recipient.id == giver.id
            for assignment in assignments
        ):
            return False

        return True

    def assign(self, giver: Person, recipient: Person) -> Assignment:
        if not self.can_assign(giver, recipient):
            raise ValueError(f"{giver.name} cannot be assigned to {recipient.name}")
        assignment = Assignment(giver=giver, recipient=recipient)
        self.assignments.append(assignment)
        return assignment

    def _attempt_generate_assignments(self) -> list[Assignment]:
        assignments: list[Assignment] = []

        for recipient in self.config.people:
            candidate_givers = [
                giver
                for giver in self.config.people
                if self.can_assign(giver, recipient, assignments)
            ]

            if not candidate_givers:
                raise AssignmentAttemptFailed

            giver_candidate = random.choice(candidate_givers)
            assignments.append(Assignment(giver=giver_candidate, recipient=recipient))

        return assignments

    def generate_assignments(self) -> list[Assignment]:
        if self.assignments:
            raise ValueError(
                "Cannot generate assignments for an event that already has assignments"
            )

        if (
                self.policy.giver_draw_mode != DrawMode.WITHOUT_REPLACEMENT
                or self.policy.recipient_draw_mode != DrawMode.WITHOUT_REPLACEMENT
        ):
            raise ValueError("Only without_replacement draw modes are currently supported")

        # TODO: detect misconfigurations to avoid infinite loops (eg all relationships excluded)
        while not self.assignments:
            try:
                self.assignments = self._attempt_generate_assignments()
            except AssignmentAttemptFailed:
                print("Draw attempt could not be completed; retrying.")

        return self.assignments

    def clear_assignments(self):
        self.assignments = []
