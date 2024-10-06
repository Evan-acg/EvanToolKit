from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QListWidgetItem,
    QListWidget,
    QRadioButton,
)
import os.path as osp
from PySide6.QtGui import QPixmap, QIcon

from app.modules.common.collector import ImageCollector
from app.modules.common.sorter import FileNameSorter


class ImageController:
    def __init__(self, root: QWidget) -> None:
        self.root: QWidget = root

        self.connects()

    def connects(self) -> None:
        select_folder_btn = self.root.findChild(QPushButton, "btn_select_folder")
        if select_folder_btn is not None:
            select_folder_btn.clicked.connect(self.select_folder_handler)

        refresh_btn = self.root.findChild(QPushButton, "btn_refresh")
        if refresh_btn is not None:
            refresh_btn.clicked.connect(self.refresh_image_handler)

    def select_folder_handler(self) -> None:
        folder_path: str = QFileDialog.getExistingDirectory(
            None, "Select Folder", osp.expanduser("~")
        )
        if folder_path == "":
            return

        inp = self.root.findChild(QLineEdit, "inp_folder")
        if inp is None:
            return
        inp.setText(folder_path)

    def refresh_image_handler(self) -> None:
        inp = self.root.findChild(QLineEdit, "inp_folder")
        if inp is None:
            return
        path = inp.text()
        if path == "":
            return
        if not osp.exists(path):
            return

        container = self.root.findChild(QListWidget, "image_list")

        if container is None:
            return

        single_depth_radio = self.root.findChild(QRadioButton, "radio_single_deeps")

        depth: int = (
            None
            if single_depth_radio is None or not single_depth_radio.isChecked()
            else 1
        )

        if single_depth_radio is None:
            return

        container.clear()

        collector = ImageCollector()
        images = collector.collect(path, depth)

        asc_radio = self.root.findChild(QRadioButton, "radio_asc")
        is_desc = False if asc_radio is None or asc_radio.isChecked() else True

        sort_by_filesize_radio = self.root.findChild(
            QRadioButton, "radio_sort_by_filesize"
        )

        sort_by = FileNameSorter()

        if sort_by_filesize_radio is not None and sort_by_filesize_radio.isChecked():
            sort_by = FileNameSorter()

        images = sort_by.sort(images, is_desc)

        for image in images:
            item = QListWidgetItem(str(image))
            pixmap = QPixmap(image).scaledToWidth(256)
            item.setIcon(QIcon(pixmap))
            item.setText(osp.basename(image))
            container.addItem(item)
