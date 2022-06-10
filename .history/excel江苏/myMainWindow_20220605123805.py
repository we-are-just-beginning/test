import sys
import pandas as pd
import os
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
        self.__filelist = []  # 存储目录下的所有mca文件全名
# ================自定义槽函数============================

    @pyqtSlot()  # “选择已有文件 ”
    def on_btnData_clicked(self):  # 为界面上的btnData按钮设置
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载文件"  # 对话框标题
        filt = "所有文件(*.*);;excel文件(*.xls*)"  # 文件过滤器
        filename, filtused = QFileDialog.getOpenFileName(
            self, dlgTitle, curPath, filt)
        self.__file_name1 = filename

# ================自定义槽函数===============================

    @pyqtSlot()  # “加载参考文件 ”
    def on_btnTxt_clicked(self):  # 为界面上的btnExcel按钮设置
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载参考文件"  # 对话框标题
        filt = "所有文件(*.*);;excel文件(*.xls*)"  # 文件过滤器
        filename, filtused = QFileDialog.getOpenFileName(
            self, dlgTitle, curPath, filt)
        self.__file_name2 = filename


# ================自定义槽函数============================

    @pyqtSlot()  # “数据处理 ”
    def on_btnHandle_clicked(self):  # 为界面上的btnHandle按钮设置

        df2 = pd.read_csv(self.__file_name, sep=' ',
                          dtype=object, encoding='gbk', header=None)
        getfilename = df2.iloc[:, 0]

        for j in range(len(getfilename)):

            if df2.iloc[0, 1][:4] == '8986':
                str_iccid = ''
                list_iccid = df2.iloc[:, 1:3].applymap(lambda x: str_iccid.join(
                    [x[k] for k in [(i + (-1) ** i) for i in range(len(x))]]))
                x = dataICCID[dataICCID.values == list_iccid.iloc[j, 0]].index
                y = dataICCID[dataICCID.values == list_iccid.iloc[j, 1]].index
                outpath = folder_path + '/' + getfilename[j]
                outpath = os.path.splitext(outpath)[0] + '.log'
                df3 = data_all.iloc[x[0]:y[0] + 1, ]
                df3.to_csv(outpath, sep='/', index=False, header=False)
            else:
                x = dataICCID[dataICCID.values == df2.iloc[j, 1]].index
                y = dataICCID[dataICCID.values == df2.iloc[j, 2]].index
                outpath = folder_path + '/' + getfilename[j]
                outpath = os.path.splitext(outpath)[0] + '.log'
                df3 = data_all.iloc[x[0]:y[0] + 1, ]
                df3.to_csv(outpath, sep='/', index=False, header=False)

        msg_box = QMessageBox(QMessageBox.Information, '处理结束', '日志处理已完成')
        msg_box.exec_()


# ================窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
