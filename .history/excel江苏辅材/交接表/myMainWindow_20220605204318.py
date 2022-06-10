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
        df1 = pd.read_excel(self.__file_name1,sheet_name=0,header=0)
        df2 = pd.read_excel(self.__file_name1,sheet_name=1,header=0)
        regions = df1['城市'].unique().tolist
        
        
        app = xw.App(visible=False, add_book=False)
        app.display_alerts = False
        app.screen_updating = False
        # workbook1 = app.books.open(self.__file_name1)
        # worksheet1 = workbook1.sheets[0]
        # worksheet2 = workbook1.sheets[1]
        # last_cell = worksheet1.used_range.last_cell
        # last_row = last_cell.row
        # last_col = last_cell.column
        # regions = set(worksheet2.range("C:C"))
        
        workbook2 = app.books.open(self.__file_name2)
        worksheet3 = workbook2.sheets['sheet1']

        
        for region in regions:
            worksheet4 = worksheet3.copy(after=worksheet3,name=region)
            # workbook2.sheets[f'{region}']
            worksheet4["G2"].value = df2[df2['城市']==region][0,17]
            worksheet4["G4"].value = df2[df2['城市']==region][0,15]
            worksheet4["G5"].value = df2[df2['城市']==region][0,16]
            worksheet4["D7"].value = df2[df2['城市']==region][0,18]            
            worksheet4["D9"].value = df2[df2['城市']==region][0,13]
            worksheet4["D11"].value = df2[df2['城市']==region][0,10]
            worksheet4["D12"].value = df2[df2['城市']==region][0,9]
            worksheet4["D13"].value = df2[df2['城市']==region][0,20]
            worksheet4["D15"].value = df2[df2['城市']==region][0,14]
            worksheet4["A19"].value = region
            worksheet4["C19"].value = df2[df2['城市']==region][0,10]
            worksheet4["D19"].value = df2[df2['城市']==region][0,9]
            
        msg_box = QMessageBox(QMessageBox.Information, '处理结束', '已完成')
        msg_box.exec_()


# ================窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
