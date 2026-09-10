import datetime
from pathlib import Path

from wishlist.models import Assignment
from wishlist.settings import settings

from .render import MermaidFlowRenderer


class AssignmentWriter:
    def __init__(self, renderer: MermaidFlowRenderer):
        self.renderer = renderer

    def write(self, assignments: list[Assignment]) -> Path:
        graph = self.renderer.render_assignments(assignments)

        runs_dir = Path(settings.run_storage_path)
        runs_dir.mkdir(parents=True, exist_ok=True)

        output_path = runs_dir / f"{int(datetime.datetime.now().timestamp() * 100)}.md"
        output_path.write_text(graph, encoding="utf-8")

        return output_path
