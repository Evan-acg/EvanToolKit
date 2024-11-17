import os
import os.path as osp

from app.common.file import FileCollector, ImageFileFilter


class TestImageCollection:

    def setup_class(self) -> None:
        self.path: str = r".\tests\resources\images"

    def setup_method(self) -> None:
        self.collector: FileCollector = FileCollector()
        self.collector.add_filter(ImageFileFilter())

    def teardown_method(self) -> None:
        del self.collector

    def test_depth_eq_1_should_work(self) -> None:

        detector = ImageFileFilter()

        example = [
            full_path
            for file in os.listdir(self.path)
            if not os.path.isdir(full_path := os.path.join(self.path, file))
            and detector.invoke(full_path)
        ]

        example_file_count = len(example)
        data_file_count = len(self.collector.invoke(self.path, 1))

        assert example_file_count == data_file_count

    def test_depth_eq_2_should_work(self) -> None:

        detector = ImageFileFilter()

        example = [
            full_path
            for root, _, files in os.walk(self.path)
            for file in files
            if detector.invoke(full_path := osp.join(root, file))
        ]

        example_file_count = len(example)
        data_file_count = len(self.collector.invoke(self.path, 2))

        assert example_file_count == data_file_count

    def test_file_not_exists_should_return_empty_list(self) -> None:
        assert self.collector.invoke("not_exists") == []

    def test_depth_eq_0_should_return_empty_list(self) -> None:
        assert self.collector.invoke(self.path, 0) == []

    def test_depth_is_str_should_return_empty_list(self) -> None:
        assert self.collector.invoke(self.path, "1") == []  # type: ignore
