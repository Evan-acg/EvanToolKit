from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import typing as t
from PySide6.QtWidgets import QWidget


@dataclass
class Event:
    name: str


class Mediator(ABC):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name
        self.component: t.Dict[str, Component] = {}

    def bind(self, component: "Component", name: str) -> None:
        self.component[name] = component

    @abstractmethod
    def on(self, event) -> None:
        pass


class Component(ABC):
    def __init__(self) -> None:
        self.mediators: t.Dict[str, Mediator] = {}
        self.widget: QWidget | None

    def subscribe(self, mediator: Mediator, name: str) -> None:
        self.mediators[name] = mediator

    def bind(self, widget: QWidget) -> None:
        self.widget = widget

    @abstractmethod
    def bind(self, widget: QWidget) -> None:
        pass

    @abstractmethod
    def invoke(self) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass
