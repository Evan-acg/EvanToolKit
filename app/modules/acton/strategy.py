from abc import ABC, abstractmethod
from os import PathLike
import os
import typing as t
import os.path as osp


ImageAcquirePayload = t.TypedDict(
    "ImageAcquirePayload",
    {
        "path": str | PathLike[str],
        "deep": t.NotRequired[bool],
        "filter": t.NotRequired[t.Callable[[str], bool]],
        "elements": t.NotRequired[t.Sequence[str]],
    },
)


P = t.TypeVar("P")


class StrategyActon(ABC, t.Generic[P]):
    def __init__(self, payload: P | None) -> None:
        self.payload: P | None = payload

    @abstractmethod
    def invoke(self) -> None:
        pass


class ActionImageAcquire(StrategyActon[ImageAcquirePayload]):
    def __init__(self, payload: ImageAcquirePayload) -> None:
        self.payload: ImageAcquirePayload = payload

    def invoke(self) -> None:
        path: str | PathLike[str] = os.path.abspath(self.payload["path"])
        is_deep: bool = self.payload.get("deep", False)
        filter_cb: t.Optional[t.Callable[[str], bool]] = self.payload.get("filter")

        if is_deep:
            self.payload["elements"] = [
                osp.join(root, file)
                for root, _, files in os.walk(path)
                for file in files
            ]
        else:
            self.payload["elements"] = [
                osp.join(path, file) for file in os.listdir(path)
            ]
        if callable(filter_cb):
            self.payload["elements"] = list(
                filter(self.payload["filter"], self.payload["elements"])
            )


class ActionImageSort(StopAsyncIteration):
    def __init__(self) -> None:
        pass

    def invoke(self) -> None:
        pass
