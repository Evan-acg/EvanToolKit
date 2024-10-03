from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QLineEdit
import os.path as osp


class FolderSelectButtonHandler:
    def __init__(self, root: QWidget) -> None:
        self.root: QWidget = root
        self.widget: QPushButton | None = self.root.findChild(
            QPushButton, "btn_select_folder"
        )

    def open_dialog(self) -> str:
        folder_path: str = QFileDialog.getExistingDirectory(
            None, "Select Folder", osp.expanduser("~")
        )
        if folder_path:
            return folder_path
        return ""

    def handler(self) -> None:
        if self.widget is None:
            return

        folder_path = self.open_dialog()
        if folder_path:
            inp = self.root.findChild(QLineEdit, "inp_folder")
            if inp is None:
                return
            inp.setText(folder_path)

    def register(self) -> None:
        if self.widget is None:
            return
        self.widget.clicked.connect(self.handler)
