"""Template related tooling."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class TemplateTools:
    """Copy project templates into a target directory."""

    def __init__(self, templates_dir: Path | None = None) -> None:
        if templates_dir is None:
            templates_dir = Path(__file__).resolve().parents[2] / "templates"
        self._templates_dir = templates_dir

    def create_project_template(self, name: str, destination: str) -> Path:
        source = (self._templates_dir / name).resolve()
        if not source.exists() or not source.is_dir():
            raise FileNotFoundError(f"Unknown template: {name}")

        dest_path = Path(destination).expanduser().resolve()
        LOGGER.info("Copying template %s to %s", source, dest_path)
        dest_path.mkdir(parents=True, exist_ok=True)

        for item in source.rglob("*"):
            relative = item.relative_to(source)
            target = dest_path / relative
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        return dest_path
