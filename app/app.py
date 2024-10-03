from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QFileDialog
from PySide6.QtUiTools import QUiLoader
import typing as t

ui_loader = QUiLoader()


def open_folder_dialog() -> str:
    folder_path: str = QFileDialog.getExistingDirectory(None, "Select Folder", "")
    if folder_path:
        return folder_path
    return ""


class EvanToolkitApp(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.ui = ui_loader.load("app/resources/EvanToolkit.ui")
        widget = self.ui.findChild(QLineEdit, "inp_folder")
        self.inp_folder: QLineEdit = t.cast(QLineEdit, widget)

        self.action_register()

    def action_register(self):
        btn_refresh = self.ui.findChild(QPushButton, "btn_refresh")
        btn_refresh.clicked.connect(self.on_refresh)

        btn_select_folder = self.ui.findChild(QPushButton, "btn_select_folder")
        btn_select_folder.clicked.connect(self.on_open_folder_select_dialog)

    def on_refresh(self) -> None:
        print("Refresh button clicked")

    def on_open_folder_select_dialog(self) -> None:
        folder_path = open_folder_dialog()
        self.inp_folder.setText(folder_path)


def main():
    app = EvanToolkitApp()
    return app
