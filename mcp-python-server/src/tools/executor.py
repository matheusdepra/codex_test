"""Command execution helpers."""
from __future__ import annotations

import logging
import shlex
import subprocess
from typing import Dict, List

LOGGER = logging.getLogger(__name__)

_ALLOWED_PREFIXES: List[List[str]] = [
    ["pip", "install"],
    ["pip3", "install"],
    ["pip", "list"],
    ["pip3", "list"],
    ["python"],
    ["python3"],
    ["ls"],
]


class ExecutorTools:
    """Run a limited subset of commands in a safe way."""

    def run_command(self, cmd: List[str]) -> Dict[str, str]:
        if not cmd:
            raise ValueError("Command list cannot be empty")

        LOGGER.info("Requested command: %s", cmd)
        if not self._is_allowed(cmd):
            raise PermissionError(
                "Command not allowed. Only simple python/pip/ls commands are permitted."
            )

        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        LOGGER.info("Command exited with %s", completed.returncode)

        return {
            "command": " ".join(shlex.quote(part) for part in cmd),
            "returncode": str(completed.returncode),
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }

    def _is_allowed(self, cmd: List[str]) -> bool:
        for prefix in _ALLOWED_PREFIXES:
            if cmd[: len(prefix)] == prefix:
                return True
        return False
