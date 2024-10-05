import os.path as osp
import typing as t

import filetype  # type: ignore


class FileTypeDetector(t.Protocol):

    def detect(self, path: str) -> bool:
        pass


class ImageFileTypeDetector:

    def detect(self, path: str) -> bool:
        if osp.isdir(path):
            return False
        kind = filetype.guess(path)
        return getattr(kind, "mime", "").startswith("image/")
