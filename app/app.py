from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from app.modules.image.blz import ImageToolBlz

ui_loader = QUiLoader()


class EvanToolkitApp(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.ui = ui_loader.load("app/resources/EvanToolkit.ui")
        self.blz = ImageToolBlz(self.ui)


def main():
    app = EvanToolkitApp()
    return app
