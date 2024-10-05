import os
import os.path as osp
import typing as t

from app.modules.common.filetype import FileTypeDetector, ImageFileTypeDetector


class FileCollector(t.Protocol):
    def collect(self, path: str, deep: bool = False) -> t.Sequence[str]:
        pass


class ImageCollector:
    detector: FileTypeDetector = ImageFileTypeDetector()

    def collect(self, path: str | os.PathLike[str], depth: int = 1) -> t.Sequence[str]:
        if not osp.exists(path):
            return []
        if not isinstance(depth, int):
            return []
        if depth < 1:
            return []

        return [
            full_path
            for root, _, files in os.walk(path)
            if root[len(str(path)) :].count(os.sep) < depth
            for file in files
            if self.detector.detect(full_path := os.path.join(root, file))
        ]
