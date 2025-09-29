from pathlib import Path
from subprocess import run
from types import TracebackType
from typing import Self


class DockerCompose:
    def __init__(self, context: Path):
        self._context = context

    def __enter__(self) -> Self:
        self._down()
        self._build()
        return self

    def __exit__(
        self,
        type: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """
        Does not remove cantainers on error.
        Use them for investigation with:
        `docker compose logs <service_name>`
        """
        if value is None:
            self._down()
        return True

    def _build(self):
        command = "docker compose -f docker-compose.yml -f docker-compose.test.yml up -d --build --wait"
        self._run(command)

    def _down(self):
        command = "docker compose down --remove-orphans"
        self._run(command)

    def _run(self, command: str):
        return run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            cwd=self._context,
        )
