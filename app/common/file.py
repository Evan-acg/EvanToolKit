import os
import os.path as osp
import typing as t
from abc import abstractmethod

import filetype  # type: ignore

from app.common import P
from app.common.action import IAction


class FileFilter(IAction):
    @abstractmethod
    def invoke(self, *args, **kwargs) -> bool:
        pass


class ImageFileFilter(FileFilter):
    def invoke(self, path: P) -> bool:
        if not osp.isfile(path):
            return False
        kind = filetype.guess(path)
        return kind is not None and kind.mime.startswith("image")


class FileCollector(IAction):
    def __init__(self) -> None:
        self.filters: t.List[FileFilter] = []

    def add_filter(self, filter: FileFilter) -> None:
        self.filters.append(filter)

    def invoke(self, path: P, depth: int = 1) -> t.Sequence[P]:
        if not osp.exists(path):
            return []

        if not isinstance(depth, int):
            return []

        return [
            os.path.join(root, file)
            for root, _, files in os.walk(path)
            for file in files
            if all(f.invoke(os.path.join(root, file)) for f in self.filters)
            and len(os.path.relpath(os.path.join(root, file), path).split(os.sep))
            <= depth
        ]


R = t.TypeVar("R", str, bytes)


class FileLoader(t.Generic[R], IAction):
    def read_as_text(self, path: P, encoding: str = "utf8") -> str:
        with open(path, "r", encoding=encoding) as f:
            return f.read()

    def read_as_bytes(self, path: P) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def invoke(self, path: P, as_text: bool = True, encoding: str = "utf8") -> R:
        if as_text:
            return t.cast(R, self.read_as_text(path, encoding=encoding))
        else:
            return t.cast(R, self.read_as_bytes(path))
