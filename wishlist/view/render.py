import datetime

from wishlist.models import Assignment

class MermaidFlowRenderer:
    def __init__(self, style="TD"):
        self.style = style

    def _generate_safe_id(self, id: str) -> str:
        return id

    def _generate_graph_components(self, assignments: list[Assignment]) -> list[str]:
        # step 1: generate the ids first
        chart_nodes = {
            f"\t{self._generate_safe_id(person.id)}[\"{person.id}\"]"
            for assignment
            in assignments
            for person in (assignment.giver, assignment.recipient)
        }

        # step 2: generate the connections
        chart_edges = {
            f"\t{self._generate_safe_id(assignment.giver.id)} --> {self._generate_safe_id(assignment.recipient.id)}"
            for assignment
            in assignments
        }

        return sorted(list(chart_nodes)) + sorted(list(chart_edges))

    def _generate_graph(self, assignments: list[Assignment]) -> list[str]:
        return [
            "```mermaid",
            f"flowchart {self.style}",
            *self._generate_graph_components(assignments),
            "```"
        ]

    def render_assignments(self, assignments: list[Assignment]) -> str:
        date_str = datetime.datetime.strftime(datetime.datetime.now(), '%m.%d.%Y')
        return "\n".join(
            [
                f"# Run for {date_str}",
                "Secret Santa Assignments:",
                "",
                *self._generate_graph(assignments),
                ""
            ]
        )



