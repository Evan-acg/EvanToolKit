import os
import typing as t

from PySide6.QtWidgets import (
    QFileDialog,
    QLineEdit,
    QListWidget,
    QPushButton,
    QListWidgetItem,
)
from PySide6.QtGui import QPixmap, QIcon

from app.modules.common.collector import ImageCollector


class Mediator(t.Protocol):
    def bind(self, *args, **kwargs) -> None:
        pass

    def acquire(self, *args, **kwargs) -> t.Any:
        pass

    def notify(self, *args, **kwargs) -> None:
        pass


class Component(t.Protocol):

    def subscribe(self, *args, **kwargs) -> None:
        pass

    def bind(self, *args, **kwargs) -> None:
        pass

    def invoke(self, *args, **kwargs) -> None:
        pass

    def notify(self, *args, **kwargs) -> None:
        pass


class FolderInputMediator:
    def __init__(self) -> None:
        self.widget: QLineEdit | None = None

    def bind(self, widget: QLineEdit | None) -> None:
        self.widget = widget

    def acquire(self) -> str:
        if self.widget is None:
            return ""
        return self.widget.text()

    def notify(self, message: str) -> None:
        if self.widget is None:
            return
        self.widget.setText(message)


class ImageStageMediator:
    def __init__(self) -> None:
        self.widget: QListWidget | None = None
        self.collector: ImageCollector = ImageCollector()

    def bind(self, widget: QListWidget | None) -> None:
        self.widget = widget

    def acquire(self) -> None:
        return

    def assemble_list_item(self, paths: t.Sequence[str]) -> t.List[QListWidgetItem]:
        items: t.List[QListWidgetItem] = []
        for path in paths:
            item: QListWidgetItem = QListWidgetItem(path)
            pix: QPixmap = QPixmap(path).scaledToWidth(256)
            item.setIcon(QIcon(pix))
            item.setText(os.path.basename(path))
            items.append(item)
        return items

    def notify(self, message: str) -> None:
        image_paths = self.collector.collect(message)
        list_items = self.assemble_list_item(image_paths)
        if self.widget is None:
            return
        self.widget.clear()
        for item in list_items:
            self.widget.addItem(item)


class FindWorkFolderButtonComp:
    def __init__(self) -> None:
        self.root_path: str = os.path.expanduser("~")

        self.mediator: t.Dict[str | None, Mediator] = {}
        self.widget: QPushButton | None = None
        self.message: str = ""

    def subscribe(self, mediator: Mediator) -> None:
        self.mediator[None] = mediator

    def bind(self, widget: QPushButton | None) -> None:
        self.widget = widget
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


class RefreshImageButtonComp:
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
        if self.mediator is None:
            return

        mediator = self.mediator.get("stage")
        if mediator is None:
            return

        mediator.notify()
