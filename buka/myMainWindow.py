import sys
import datetime as dt
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
        self.__dir_path = None
        self.__file_name = None
        self.__filelist = []  # 存储目录下的所有mca文件全名
# ================自定义槽函数============================

    @pyqtSlot()  # “选择已有目录 ”
    def on_btnData_clicked(self):  # 为界面上的btnData按钮设置
        self.__filelist.clear()
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载数据"  # 对话框标题
        dir_path = QFileDialog.getExistingDirectory(self,
                                                    dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        self.__dir_path = dir_path
        filenames = os.listdir(dir_path)  # 获得文件夹内所有文件
        for filename in filenames:
            file_type = filename.split('.')[-1]  # 截取后缀

            if (file_type == 'MCA') or (file_type == 'mca'):
                self.__filelist.append(filename)

# ================自定义槽函数===============================

    @pyqtSlot()  # “加载补卡文件 ”
    def on_btnTxt_clicked(self):  # 为界面上的btnExcel按钮设置
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载补卡文件"  # 对话框标题
        filt = "所有文件(*.*);;txt文件(*.txt)"  # 文件过滤器
        filename, filtused = QFileDialog.getOpenFileName(
            self, dlgTitle, curPath, filt)  # 带路径的文件名
        self.__file_name = filename


# ================自定义槽函数============================

    @pyqtSlot()  # “数据处理 ”
    def on_btnHandle_clicked(self):  # 为界面上的btnHandle按钮设置

        df_all = []
        append = df_all.append
        for file in self.__filelist:
            df = pd.read_csv(self.__dir_path + '/' + file, header=0, dtype=object,
                             encoding='ANSI')  # 读取mca数据成DataFrame
            append(df)  # 多个df的list

        data_all = pd.concat(df_all)  # concat:合并，将多个DataFrame合并为一个
        data_all.dropna()  # 删除全部空行
        data_all = data_all.reset_index(drop=True)  # 重置索引

        df2 = pd.read_csv(self.__file_name,
                          dtype=object, encoding='utf-8', header=0)  # 读取补卡文件
        '''
        两种补卡模式;
        ICCID模式:  必须是20位,字符需要两两倒置,再筛选；
        打印项模式:  必须保证补卡文件中ICCID号段的格式与MCA数据中的打印项格式一致;
                    普通卡/远程卡都可以,多少位都可以；
        '''
        # if df2.iloc[0, 0][:4] == '8986':  # 判断是否普通卡
        #     if df2.columns[0][:4] == '打印数据':  # 判断补卡模式为'打印数据'模式
        #         result_data = pd.merge(
        #             data_all, df2, on=(df2.columns.values.tolist()))
        #         # 按补卡文件筛选补卡数据，pd.merge用法，取交集

        #     elif len(df2.iloc[0, 0]) == 20:  # 判断普通卡ICCID是否20位
        #         list_iccid = df2.applymap(lambda x: ''.join(
        #             [x[k] for k in [(i + (-1) ** i) for i in range(len(x))]]))  # 字符两两倒置
        #         result_data = pd.merge(
        #             data_all, list_iccid, on=(df2.columns.values.tolist()))
        #     else:
        #         msg_box = QMessageBox(
        #             QMessageBox.Warning, '警告', "普通卡必须是20位,否则请参考说明按'打印数据'筛选补卡")
        #         msg_box.exec_()
        #         sys.exit(0)  # 退出程序
        # else:
        #     result_data = pd.merge(
        #         data_all, df2, on=(df2.columns.values.tolist()))
        if (df2.iloc[0, 0][:4] != '8986') or (df2.columns[0][:4] == '打印数据'):  # 判断是否普通卡
            result_data = pd.merge(
                data_all, df2, on=(df2.columns.values.tolist()))
        elif (df2.iloc[0, 0][:4] == '8986') and (len(df2.iloc[0, 0])) == 20:
            list_iccid = df2.applymap(lambda x: ''.join(
                [x[k] for k in [(i + (-1) ** i) for i in range(len(x))]]))  # 字符两两倒置
            result_data = pd.merge(
                data_all, list_iccid, on=(df2.columns.values.tolist()))

        folder_path = self.__dir_path + '/' + '补卡'
        strdatetime = dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')  # 获取系统时间

        if os.path.isdir(folder_path):  # 判断目录是否存在
            result_data.to_csv(folder_path + '/' + strdatetime + '_补卡.mca',
                               index=False, header=True, encoding='ANSI')  # 输出补卡数据
        else:
            os.makedirs(folder_path)  # 创建目录
            result_data.to_csv(folder_path + '/' + strdatetime + '_补卡.mca',
                               index=False, header=True, encoding='ANSI')
        msg_box = QMessageBox(QMessageBox.Information, '处理结束', '补卡处理已完成')
        msg_box.exec_()


# ================窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
