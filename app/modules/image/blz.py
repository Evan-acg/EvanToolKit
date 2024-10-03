import typing as t

from PySide6.QtWidgets import QWidget

from app.modules.image.event.button_select_folder import \
    FolderSelectButtonHandler


class ImageToolBlz:
    def __init__(self, win: QWidget) -> None:
        self.win: QWidget = win
        self.handlers: t.List = []

        self.handler_register()

    def handler_register(self) -> None:
        handlers = [FolderSelectButtonHandler]
        for H in handlers:
            handler = H(self.win)
            handler.register()
            self.handlers.append(handler)
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

        ...


# 使用事件总线机制进行代理
# 使用组合模式将这些事件进行分解
