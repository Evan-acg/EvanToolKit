import os
import filetype  # type: ignore
import pytest

from app.modules.image.strategy import ImageAcquirePayload, ActionImageAcquire


@pytest.mark.skip(reason="utils function")
def test_image(path):
    if os.path.isdir(path):
        return False
    kind = filetype.guess(path)
    return kind is not None and kind.mime.startswith("image")


@pytest.fixture(autouse=True)
def payload() -> ImageAcquirePayload:
    return {
        "path": r"./tests/resources/images",
        "elements": [],
    }


class TestImageAcquire:

    def test_should_be_list_of_images_path(self, payload: ImageAcquirePayload) -> None:
        strategy = ActionImageAcquire(payload)
        strategy.invoke()
        assert len(payload["elements"]) > 0

    def test_should_be_list_only_images_path(
        self, payload: ImageAcquirePayload
    ) -> None:
        payload["filter"] = lambda x: test_image(x)
        path: str | os.PathLike[str] = payload["path"]

        actual_elements = [
            image_path
            for file in os.listdir(path)
            if test_image(image_path := os.path.join(path, file))
        ]

        strategy = ActionImageAcquire(payload)
        strategy.invoke()
        assert len(payload["elements"]) == len(actual_elements)

    def test_should_be_list_only_images_path_deep(
        self, payload: ImageAcquirePayload
    ) -> None:

        path: str | os.PathLike[str] = payload["path"]
        payload["filter"] = lambda x: test_image(x)
        payload["deep"] = True

        actual_elements = [
            image_path
            for root, _, files in os.walk(path)
            for file in files
            if test_image(image_path := os.path.join(root, file))
        ]

        strategy = ActionImageAcquire(payload)
        strategy.invoke()
        assert len(payload["elements"]) == len(actual_elements)
