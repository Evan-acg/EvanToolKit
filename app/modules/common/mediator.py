from abc import ABC, abstractmethod
from enum import Enum
import os
from turtle import width
import typing as t
from concurrent.futures import ThreadPoolExecutor, as_completed

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QWidget,
)

from app.modules.common.collector import ImageCollector
from app.modules.event import Component, Mediator



class FolderInputMediator(Mediator):

    def acquire(self) -> str:
        widget: QLineEdit | None = t.cast(QLineEdit, self.widgets.get(None))
        if widget is None:
            return ""
        return widget.text()

    def notify(self, message: str) -> None:
        widget: QLineEdit | None = t.cast(QLineEdit, self.widgets.get(None))
        if widget is None:
            return
        widget.setText(message)


class ImageStageMediator(Mediator):
    class Comp(Enum):
        BUTTON = "BUTTON"
        STAGE = "STAGE"

    def __init__(self) -> None:
        self.collector: ImageCollector = ImageCollector()

    def acquire(self) -> None:
        return

    def _build_list_item(self, path: str):
        item: QListWidgetItem = QListWidgetItem(path)
        pix: QPixmap = QPixmap(path).scaledToWidth(256)
        item.setIcon(QIcon(pix))
        item.setText(os.path.basename(path))
        return item

    def assemble_list_item(self, paths: t.Sequence[str]) -> None:
        widget: QListWidget | None = t.cast(
            QListWidget, self.widgets.get(self.Comp.STAGE)
        )
        if widget is None:
            return
        widget.clear()
        with ThreadPoolExecutor() as executor:
            tasks = [executor.submit(self._build_list_item, path) for path in paths]

        for result in as_completed(tasks):
            widget.addItem(result.result())

    def notify(self, message: str) -> None:
        image_paths = self.collector.collect(message)
        self.assemble_list_item(image_paths)



class SortByFilenameRadioComp:
    def __init__(self) -> None:
        self.mediator: t.Dict[str | None, Mediator] = {}
        self.widget: QRadioButton | None = None

    def subscribe(self, mediator: Mediator, name: str | None) -> None:
        self.mediator[name] = mediator

    def bind(self, widget: t.Any) -> None:
        self.widget = widget
        if widget is None:
            return
        widget.checked.connect(self.invoke)

    def invoke(self) -> None:
        pass

    def notify(self) -> None:
        mediator = self.mediator.get(None)
        if mediator is None:
            return
        mediator.notify()


class SortByFileSizeRadioComp:
    def subscribe(self) -> None:
        pass

    def bind(self) -> None:
        pass

    def invoke(self) -> None:
        pass

    def notify(self) -> None:
        pass


class SortAsAccRadioComp:
    def subscribe(self) -> None:
        pass

    def bind(self) -> None:
        pass

    def invoke(self) -> None:
        pass

    def notify(self) -> None:
        pass


class SortAsDescRadioComp:
    def subscribe(self) -> None:
        pass

    def bind(self) -> None:
        pass

    def invoke(self) -> None:
        pass

    def notify(self) -> None:
        pass
