import os
import os.path as osp
import typing as t



# class TestFileNameSorter:
#     def setup_method(self) -> None:
#         self.sorter: Sorter = FileNameSorter()

#     def test_filename_sorter_ascending(self) -> None:
#         experimental: t.Sequence[str] = ["file3.txt", "file1.txt", "file2.txt"]
#         control: t.Sequence[str] = ["file1.txt", "file2.txt", "file3.txt"]
#         result: t.Sequence[str] = self.sorter.sort(experimental)
#         assert result == control

#     def test_filename_sorter_descending(self) -> None:
#         experimental: t.Sequence[str] = ["file3.txt", "file1.txt", "file2.txt"]
#         control: t.Sequence[str] = ["file3.txt", "file2.txt", "file1.txt"]
#         result: t.Sequence[str] = self.sorter.sort(experimental, reverse=True)
#         assert result == control

#     def test_filename_sorter_empty_list(self) -> None:
#         experimental: t.Sequence[str] = []
#         control: t.Sequence[str] = []
#         result: t.Sequence[str] = self.sorter.sort(experimental)
#         assert result == control

#     def test_filename_sorter_single_element(self) -> None:
#         experimental: t.Sequence[str] = ["file1.txt"]
#         control: t.Sequence[str] = ["file1.txt"]
#         result: t.Sequence[str] = self.sorter.sort(experimental)
#         assert result == control


# class TestSizeSorter:
#     def setup_method(self) -> None:
#         path: str = r".\tests\resources\images"
#         self.sorter: Sorter = FileSizeSorter()
#         self.experimental: t.Sequence[str] = [
#             osp.join(path, file) for file in os.listdir(path)
#         ]

#     def teardown_method(self) -> None:
#         del self.sorter
#         del self.experimental

#     def test_size_sorter_ascending(self) -> None:
#         control: t.Sequence[str] = sorted(self.experimental, key=osp.getsize)
#         result: t.Sequence[str] = self.sorter.sort(self.experimental)
#         assert result == control

#     def test_size_sorter_descending(self) -> None:
#         control: t.Sequence[str] = sorted(
#             self.experimental, key=osp.getsize, reverse=True
#         )
#         result: t.Sequence[str] = self.sorter.sort(self.experimental, reverse=True)
#         assert result == control

#     def test_size_sorter_empty_list(self) -> None:
#         experimental: t.Sequence[str] = []
#         control: t.Sequence[str] = []
#         result: t.Sequence[str] = self.sorter.sort(experimental)
#         assert result == control
