from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Slot
from pathlib import Path
import os
from yaml import mkdocsYAML


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
        self.ui.buildButton.clicked.connect(self.build)
        self.ui.batchbuildButton.clicked.connect(self.batch_build)

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

    def build(self):
        """
        source 为源文件夹，在 dest 下创建同名文件夹存放 html
        """
        source = Path(self.ui.source.text())
        dest = Path(self.ui.destination.text()) / source.name
        if not dest.exists():
            dest.mkdir()
        # Show the message box and get the user's response
        msg = str(source) + "\n------>\n" + str(dest)
        msgBox = QMessageBox(QMessageBox.Question, "Confirm Paths", msg,
                             QMessageBox.Yes | QMessageBox.No)
        reply = msgBox.exec_()
        # Check if the user clicked yes
        if reply == QMessageBox.Yes:
            my = mkdocsYAML(site_name=source.name,
                            site_dir=dest,
                            docs_dir=source)
            my.build()
            QMessageBox(QMessageBox.Information, "Success", "Build completed.",
                        QMessageBox.Ok).exec_()

    def batch_build(self):
        """
        source 下面的文件夹依次是文档文件夹，在 dest 下创建同名文件夹存放 html
        """
        for i in os.scandir(self.ui.source.text()):
            if not i.is_dir() or i.name.startswith(".") or i.name == "assets":
                continue
            source = Path(i)
            dest = Path(self.ui.destination.text()) / source.name
            if not dest.exists():
                dest.mkdir()
            # Show the message box and get the user's response
            msg = str(source) + "\n------>\n" + str(dest)
            msgBox = QMessageBox(QMessageBox.Question, "Confirm Paths", msg,
                                 QMessageBox.Yes | QMessageBox.No)
            reply = msgBox.exec_()
            # Check if the user clicked yes
            if reply == QMessageBox.Yes:
                my = mkdocsYAML(site_name=source.name,
                                site_dir=dest,
                                docs_dir=source)
                my.build()
        QMessageBox(QMessageBox.Information, "Success", "Build all completed.",
                    QMessageBox.Ok).exec_()


if __name__ == "__main__":
    # 切换工作路径到脚本所在文件夹
    os.chdir(Path(__file__).absolute().parent)
    window = Window()