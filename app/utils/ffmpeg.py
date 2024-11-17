import os
import os.path as osp
import subprocess
import typing as t

from app.common.action import IAction

CommandResult = t.TypedDict(
    "CommandResult", {"stdout": str, "stderr": str, "code": int}
)

IS_DEBUG_KEY = "DEBUG"


def shell_link(link: str) -> str:
    if not link.startswith('"'):
        link = f'"{link}'
    if not link.endswith('"'):
        link = f'{link}"'
    return link


class FfmpegProcessor(IAction):
    def __init__(self) -> None:
        self.main_command: str = ""
        self.options: list[tuple[str, str]] = []

    def ffmpeg(self) -> t.Self:
        self.main_command = "ffmpeg"
        return self

    def ffprobe(self) -> t.Self:
        self.main_command = "ffprobe"
        return self

    @property
    def command(self) -> str:
        options: list[str] = [f"{key} {value}" for key, value in self.options]
        return f"{self.main_command} {' '.join(options)}"

    def option(self, key: str, value: str, prefix: str = "-") -> t.Self:
        if osp.isabs(value):
            value = shell_link(value)
        self.options.append((prefix + key, value))
        return self

    def execute(
        self, command: str, encoding: str = "utf-8", verbose: bool = False
    ) -> CommandResult:
        if verbose:
            print(f"Executing command: {command}")

        process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=encoding,
        )
        if verbose:
            print(f"Return code: {process.returncode}")
            print(f"stdout: {process.stdout}")
        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "code": process.returncode,
        }

    def invoke(self, verbose: bool | None = None) -> CommandResult:
        valid_commands: list[str] = ["ffmpeg", "ffprobe"]
        if self.main_command not in valid_commands:
            raise ValueError(
                "The command must start with 'ffmpeg' or 'ffprobe', Please use 'ffmpeg' or 'ffprobe' method to set the command."
            )
        if verbose is None:
            verbose = os.getenv(IS_DEBUG_KEY, "False").lower() in ("true", "1")
        return self.execute(self.command, verbose=verbose)
