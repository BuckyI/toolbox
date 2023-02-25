from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Slot
import os


class Window():
    def __init__(self):
        app = QApplication([])
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('window.ui')

        # self.ui.button.clicked.connect(self.handleCalc)
        self.ui.select_source.clicked.connect(lambda: self.set_folder(0))
        self.ui.select_dest.clicked.connect(lambda: self.set_folder(1))

        self.ui.show()
        app.exec_()

    def set_folder(self, index):
        FileDirectory = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        if index == 0:
            self.ui.source.setText(FileDirectory)
            print(FileDirectory)
        elif index == 1:
            self.ui.destination.setText(FileDirectory)
            print(FileDirectory)

    # def handleCalc(self):
    #     pass


if __name__ == "__main__":
    # 切换工作路径到脚本所在文件夹
    scr_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(scr_path)
    window = Window()