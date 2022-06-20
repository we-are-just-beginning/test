import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QMessageBox,QInputDialog)
from PyQt5.QtCore import pyqtSlot, QDir
from ui_MainWindow import Ui_MainWindow


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面

    def on_btnTxt_clicked(self):
        # text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:")
        # if okPressed and text != '':
        print(text)
            
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())