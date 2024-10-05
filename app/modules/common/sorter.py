import os
import typing as t
import os.path as osp


class Sorter(t.Protocol):
    def sort(self, files: t.Sequence[str], reverse: bool = False) -> t.Sequence[str]:
        pass


class FileNameSorter:
    def sort(self, files: t.Sequence[str], reverse: bool = False) -> t.Sequence[str]:
        return sorted(files, reverse=reverse)


class FileSizeSorter:
    def sort(self, files: t.Iterable[str], reverse: bool = False) -> t.Sequence[str]:
        return sorted(files, key=osp.getsize, reverse=reverse)
