import os
import os.path as osp
import typing as t
from enum import Enum

from PySide6.QtWidgets import QFileDialog, QPushButton

from app.modules.event import Component, Mediator


class FindWorkFolderButtonComp(Component):
    def __init__(self) -> None:
        self.root_path: str = osp.expanduser("~")
        self.message: str = ""

    def bind(self, widget: QPushButton | None, name: Enum | None) -> None:
        self.widgets[name] = widget
        if widget is None:
            return

        widget.clicked.connect(self.invoke)

    def invoke(self) -> None:
        path: str = QFileDialog.getExistingDirectory(
            None, "Select Folder", self.root_path
        )
        if path == "":
            return
        self.message = path
        self.notify()

    def notify(self) -> None:
        mediator = self.mediator.get(None)
        if mediator is None:
            return
        mediator.notify(self.message)


class RefreshImageButtonComp(Component):
    def __init__(self) -> None:
        self.mediator: t.Dict[str | None, Mediator] = {}
        self.widget: QPushButton | None = None

    def subscribe(self, mediator: Mediator, name: str) -> None:
        self.mediator[name] = mediator

    def bind(self, widget: t.Any) -> None:
        self.widget = widget
        if widget is None:
            return
        widget.clicked.connect(self.invoke)

    def invoke(self) -> None:
        button_mediator = self.mediator.get("button")
        stage_mediator = self.mediator.get("stage")
        if button_mediator is None:
            return

        path: str = button_mediator.acquire()

        if stage_mediator is None:
            return

        stage_mediator.notify(path)

    def notify(self) -> None:
        mediator = self.mediator.get("stage")
        if mediator is None:
            return

        mediator.notify()
