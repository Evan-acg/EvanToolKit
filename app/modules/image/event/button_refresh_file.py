from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit


class EventRadioSingleLayer:
    def __init__(self, root: QWidget) -> None:
        self.root: QWidget = root

    def handler(self) -> None:
        inp_widget = self.root.findChild(QLineEdit, "inp_folder")
        # folder_path = inp_widget.text()
        folder_path: str = r"\\Eden_ds\sex\日本\图集\@仓木麻衣@青野真衣@くらき まい"
        

    def register(self) -> None:
        widget = self.root.findChild(QPushButton, "btn_refresh")
        if widget is None:
            return
        widget.clicked.connect(self.handler)
