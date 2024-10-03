import os
import typing as t

import filetype
from PySide6.QtUiTools import QUiLoader

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QRadioButton,
)
import os.path as osp


ui_loader = QUiLoader()


def open_folder_dialog() -> str:
    folder_path: str = QFileDialog.getExistingDirectory(
        None, "Select Folder", osp.expanduser("~")
    )
    if folder_path:
        return folder_path
    return ""


def is_image(path: str) -> bool:
    kind = filetype.guess(path)
    return getattr(kind, "mime", "").startswith("image/")


class EvanToolkitApp(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.ui = ui_loader.load("app/resources/EvanToolkit.ui")
        widget = self.ui.findChild(QLineEdit, "inp_folder")
        self.inp_folder: QLineEdit = t.cast(QLineEdit, widget)

        self.button_action_register()

    def action_register(self, actions) -> None:
        for widget_type, widget_name, callback in actions:
            widget = self.ui.findChild(widget_type, widget_name)

            if widget is None:
                continue
            widget.clicked.connect(callback)

    def button_action_register(self):
        actions = [
            (QPushButton, "btn_refresh", self.on_refresh),
            (QPushButton, "btn_select_folder", self.on_open_folder_select_dialog),
        ]
        self.action_register(actions)

    def on_refresh(self) -> None:
        folder_path: str = self.inp_folder.text()
        if not folder_path:
            QMessageBox.warning(self.ui, "Warning", "请先选择文件夹")
            return
        if not osp.exists(folder_path):
            QMessageBox.warning(self.ui, "Warning", "文件夹不存在")
            return

        radio = self.ui.findChild(QRadioButton, "radio_multiple_deeps")
        is_deeps = radio.isChecked() if hasattr(radio, "isChecked") else False

        if is_deeps:
            image_paths = [
                osp.join(root, file)
                for root, dirs, files in os.walk(folder_path)
                for file in files
            ]
        else:
            image_paths = [
                osp.join(folder_path, file) for file in os.listdir(folder_path)
            ]
        for image_path in image_paths:
            if is_image(image_path):
                print(image_path)

    def on_open_folder_select_dialog(self) -> None:
        folder_path = open_folder_dialog()
        if folder_path:
            self.inp_folder.setText(folder_path)


def main():
    app = EvanToolkitApp()
    return app
