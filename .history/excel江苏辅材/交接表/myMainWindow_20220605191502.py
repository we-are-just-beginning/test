import sys
import pandas as pd
import xlwings as xw
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSlot, QDir
from ui_MainWindow import Ui_MainWindow


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.__file_name1 = None
        self.__file_name2 = None

# ================自定义槽函数============================

    @pyqtSlot()  # “选择已有文件 ”
    def on_btnData_clicked(self):  # 为界面上的btnData按钮设置
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载标签数据"  # 对话框标题
        filt = "所有文件(*.*);;excel文件(*.xls*)"  # 文件过滤器
        filename, filtused = QFileDialog.getOpenFileName(
            self, dlgTitle, curPath, filt)
        self.__file_name1 = filename

# ================自定义槽函数===============================

    @pyqtSlot()  # “加载参考文件 ”
    def on_btnTxt_clicked(self):  # 为界面上的btnExcel按钮设置
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载交接表"  # 对话框标题
        filt = "所有文件(*.*);;excel文件(*.xls*)"  # 文件过滤器
        filename, filtused = QFileDialog.getOpenFileName(
            self, dlgTitle, curPath, filt)
        self.__file_name2 = filename


# ================自定义槽函数============================

    @pyqtSlot()  # “数据处理 ”
    def on_btnHandle_clicked(self):  # 为界面上的btnHandle按钮设置
        app = xw.App(visible=False, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        workbook1 = app.books.open(r'F:\pythonProject\Data\R0220875\BZ094广东小卡.xls')
        worksheet1 = workbook1.sheets['sheet1']
        workbook2 = app.books.open(r'F:\pythonProject\Data\R0220875\广东移动.xls')
        worksheet2 = workbook2.sheets['0盒签(按地市)']
        worksheet3 = workbook2.sheets['0箱签(按地市)']
        msg_box = QMessageBox(QMessageBox.Information, '处理结束', '已完成')
        msg_box.exec_()


# ================窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
