from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget


class IHandler(ABC):
    def __init__(self, root: QWidget) -> None:
        self.root: QWidget = root

    @abstractmethod
    def register(self) -> None:
        pass
