from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QPushButton

from app.modules.common.mediator import Mediator


class SelectFolderButtonHandler(QObject):
    after = Signal(str)

    def __init__(self) -> None:
        self.mediator: Mediator | None = None
        self.widget: QPushButton | None = None
    
    def bind(self, mediator: Mediator) -> None:
        self.mediator = mediator

    def todo(self) -> None:
        if self.mediator is None:
            return
        if self.widget is None:
            return
        self.mediator.notify(self.widget, message="Hello World")

    def register(self, widget: QPushButton | None, mediator: Mediator) -> None:
        if widget is None:
            return
        self.mediator = mediator
        self.widget = widget
        widget.clicked.connect(self.todo)
