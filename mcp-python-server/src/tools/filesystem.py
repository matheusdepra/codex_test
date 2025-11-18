"""Filesystem tool implementations for the MCP server."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

LOGGER = logging.getLogger(__name__)


class FilesystemTools:
    """Provide safe helpers for reading and writing files."""

    def read_file(self, path: str) -> str:
        file_path = Path(path).expanduser().resolve()
        LOGGER.info("Reading file: %s", file_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        file_path = Path(path).expanduser().resolve()
        LOGGER.info("Writing file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    def update_file(self, path: str, content: str) -> None:
        file_path = Path(path).expanduser().resolve()
        LOGGER.info("Updating file: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Cannot update missing file: {file_path}")
        file_path.write_text(content, encoding="utf-8")

    def list_directory(self, path: str) -> List[str]:
        directory = Path(path).expanduser().resolve()
        LOGGER.info("Listing directory: %s", directory)
        if not directory.exists() or not directory.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")
        return sorted(entry.name for entry in directory.iterdir())
