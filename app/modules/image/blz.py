import typing as t

from PySide6.QtWidgets import QPushButton, QWidget, QLineEdit, QListWidget

from app.modules.common.mediator import (
    FindWorkFolderButtonComp,
    FolderInputMediator,
    ImageStageMediator,
    RefreshImageButtonComp,
)


folder_input_mediator = FolderInputMediator()
image_stage_mediator = ImageStageMediator()

find_folder_button_comp = FindWorkFolderButtonComp()
refresh_image_button_comp = RefreshImageButtonComp()


class ImageToolBlz:
    def __init__(self, win: QWidget) -> None:
        self.win: QWidget = win

        self.handler_register()

    def handler_register(self) -> None:
        folder_input_mediator.bind(self.win.findChild(QLineEdit, "inp_folder"))
        image_stage_mediator.bind(self.win.findChild(QListWidget, "image_list"))

        find_folder_button_comp.subscribe(folder_input_mediator)
        find_folder_button_comp.bind(
            self.win.findChild(QPushButton, "btn_select_folder")
        )

        refresh_image_button_comp.subscribe(folder_input_mediator, "button")
        refresh_image_button_comp.subscribe(image_stage_mediator, "stage")
        refresh_image_button_comp.bind(self.win.findChild(QPushButton, "btn_refresh"))


# 1. 注册文件夹单层radio按钮事件
# 2。 注册文件夹递归radio按钮事件
# 3. 注册文件夹选择按钮事件
# 4. 注册文件夹刷新按钮事件
# 5. 注册排序升序radio按钮事件
# 6. 注册排序降序radio按钮事件
# 7. 注册根据文件名排序radio按钮事件
# 8. 注册根据文件大小排序radio按钮事件
# 9. 注册根据拍摄修改照片文件名事件
# 10。 注册文件移动事件
