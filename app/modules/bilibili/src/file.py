import os
import os.path as osp

from app.common import P
from app.common.action import IAction
from app.common.file import FileFilter


class Ef2FileFilter(FileFilter):
    def invoke(self, file_path: P) -> bool:
        allow_ext = [".ef2", ".EF2"]
        ext: str = osp.splitext(file_path)[1]
        return ext in allow_ext


class MediaFileExactlyName(IAction):
    medias: dict[str, dict[str, str]] = {}

    def invoke(self, file_path: P) -> P:
        filename, _ = osp.splitext(osp.basename(file_path))
        if filename in self.medias:
            info = self.medias[filename]
            return info["filename"]

        folder: str = osp.dirname(file_path)
        for fn in os.listdir(folder):
            n, e = osp.splitext(fn)
            self.medias[n] = {
                "filename": osp.abspath(osp.join(folder, fn)),
                "ext": e,
                "name": n,
            }
        if filename in self.medias:
            info = self.medias[filename]
            return info["filename"]
        return ""
