import os
import os.path as osp
import typing as t

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QGroupBox,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QRadioButton,
)

from app.modules.acton.strategy import ActionImageAcquire, ImageAcquirePayload
from app.modules.image.event import IHandler
from app.utils.image import is_image
from app.utils.pyqt import find_element


class FolderRefreshButtonHandler(IHandler):

    def find_images(self, path: str, deep: bool):
        image_payload: ImageAcquirePayload = {
            "deep": deep,
            "path": path,
            "elements": [],
            "filter": lambda x: is_image(x),
        }

        action = ActionImageAcquire(image_payload)
        action.invoke()
        return image_payload["elements"]

    def sort_images(self, items: t.Sequence[str | os.PathLike[str]], is_desc: bool):
        sorted_by: str = ""
        sort_action_map = {
            "radio_sort_by_filename": lambda x: osp.basename(x),
            "radio_sort_by_filesize": lambda x: osp.getsize(x),
        }

        radio_container = self.root.findChild(QGroupBox, "sort_by_zone")
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

        return sorted(items, key=sort_action_map[sorted_by], reverse=is_desc)

    def append_list_item_to_container(
        self, container: QListWidget, items: t.Sequence[str | os.PathLike[str]]
    ) -> None:
        container.clear()
        for image_path in items:
            item = QListWidgetItem(str(image_path))
            pixmap = QPixmap(image_path).scaledToWidth(256)
            item.setIcon(QIcon(pixmap))
            item.setText(osp.basename(image_path))
            container.addItem(item)

    def handler(self) -> None:
        inp_widget = self.root.findChild(QLineEdit, "inp_folder")
        # folder_path = inp_widget.text()
        folder_path: str = r"\\Eden_ds\sex\日本\图集\@仓木麻衣@青野真衣@くらき まい"

        is_deeps: bool = find_element(
            self.root, QRadioButton, "radio_multiple_deeps", "isChecked", False
        )
        is_desc = find_element(
            self.root, QRadioButton, "radio_desc", "isChecked", False
        )

        if not folder_path:
            QMessageBox.warning(self.root, "Warning", "请先选择文件夹")
            return
        if not osp.exists(folder_path):
            QMessageBox.warning(self.root, "Warning", "文件夹不存在")
            return

        image_paths = self.find_images(folder_path, is_deeps)
        image_paths = self.sort_images(image_paths, is_desc)

        container: QListWidget | None = self.root.findChild(QListWidget, "image_list")

        if container is None:
            return

        self.append_list_item_to_container(container, image_paths)

    def register(self) -> None:
        widget = self.root.findChild(QPushButton, "btn_refresh")
        if widget is None:
            return
        widget.clicked.connect(self.handler)
