from abc import ABC
import typing as t


class IAction(ABC):
    def invoke(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        pass
