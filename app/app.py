import os
import os.path as osp
import typing as t

import filetype  # type: ignore
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QGroupBox,
)

from app.modules.image.strategy import ImageAcquirePayload, ActionImageAcquire

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


def find_element(root, type, name, cb_name, default):
    widget = root.findChild(type, name)
    if widget is None:
        return default
    if hasattr(widget, cb_name):
        return getattr(widget, cb_name)()


class EvanToolkitApp(QApplication):
    def __init__(self) -> None:
        super().__init__([])
        self.ui = ui_loader.load("app/resources/EvanToolkit.ui")
        widget = self.ui.findChild(QLineEdit, "inp_folder")
        self.inp_folder: QLineEdit = t.cast(QLineEdit, widget)

        self.inp_folder.setText(
            r"\\Eden_ds\sex\日本\图集\@仓木麻衣@青野真衣@くらき まい"
        )

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

        is_deeps = find_element(
            self.ui, QRadioButton, "radio_multiple_deeps", "isChecked", False
        )

        image_payload: ImageAcquirePayload = {
            "deep": is_deeps,
            "path": folder_path,
            "elements": [],
            "filter": lambda x: is_image(x),
        }

        action = ActionImageAcquire(image_payload)
        action.invoke()

        image_paths = image_payload["elements"]

        sort_action_map = {
            "radio_sort_by_filename": lambda x: osp.basename(x),
            "radio_sort_by_filesize": lambda x: osp.getsize(x),
        }

        is_desc = find_element(self.ui, QRadioButton, "radio_desc", "isChecked", False)
        sorted_by = ""

        radio_container = self.ui.findChild(QGroupBox, "sort_by_zone")
        if radio_container is not None:
            radios: t.Iterable[QRadioButton | None] = radio_container.findChildren(
                QRadioButton
            )
            for radio in radios:
                if radio is None:
                    continue
                if radio.isChecked():
                    sorted_by = radio.objectName()
                    break

        image_paths = sorted(
            image_paths, key=sort_action_map[sorted_by], reverse=is_desc
        )

        container: QListWidget | None = self.ui.findChild(QListWidget, "image_list")

        if container is None:
            return

        container.clear()

        for image_path in image_paths:
            print(image_path)
            item = QListWidgetItem(image_path)
            pixmap = QPixmap(image_path).scaledToWidth(256)
            item.setIcon(QIcon(pixmap))
            item.setText(osp.basename(image_path))
            container.addItem(item)

    def on_open_folder_select_dialog(self) -> None:
        folder_path = open_folder_dialog()
        if folder_path:
            self.inp_folder.setText(folder_path)


def main():
    app = EvanToolkitApp()
    return app
