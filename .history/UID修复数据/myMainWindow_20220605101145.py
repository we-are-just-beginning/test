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
        self.__dir_path = None
        self.__file_name = None
        self.__filelist = []  # 存储目录下的所有mca文件全名
# ================自定义槽函数============================

    @pyqtSlot()  # “选择已有目录 ”
    def on_btnData_clicked(self):  # 为界面上的btnData按钮设置

        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "加载数据"  # 对话框标题
        dir_path = QFileDialog.getExistingDirectory(self,
                                                    dlgTitle, curPath, QFileDialog.ShowDirsOnly)
        self.__dir_path = dir_path
        filenames = os.listdir(dir_path)  # 获得文件夹内所有文件
        for filename in filenames:
            file_type = filename.split('.')[-1]
            if file_type == 'log':
                self.__filelist.append(filename)



# ================自定义槽函数============================

    @pyqtSlot()  # “数据处理 ”
    def on_btnHandle_clicked(self):  # 为界面上的btnHandle按钮设置
         for file in self.__filelist:
            df = pd.read_csv(self.__dir_path + '/' + file, sep='/', names=['ICCID', 'SEID', 'UID', '打印项'], header=None, dtype=object,
                             encoding='utf-8')  # 读取mca数据成DataFrame
            df.dropna()  # 删除全部空行
            df = df.reset_index(drop=True)  # 重置索引
            df.insert(loc=0, column='OLDICCID', value=df['ICCID']) #插入OLDICCID列
            df2 = df['打印项'].str.split(',', expand=True)  # 按逗号拆分
            df2.rename(columns={0: '打印数据1', 1: '打印数据2', 2: '打印数据3', 3: '打印数据4'}, inplace=True) #打印项重命名
            df2.drop(columns=4, inplace=True)  # 删除最后一列空白
            df.drop(columns=['打印项'], inplace=True)  # 删除原来的打印项
            data = pd.concat([df, df2], axis=1)  # 横向连接
            outfile = os.path.splitext(file)[0] + '_修复.mca'

            outpath=os.path.join(path,'修复数据',outfile)

            if os.path.isdir(path + './修复数据'):
                data.to_csv(outpath,
                        sep=',', index=False, header=True, encoding='ANSI')
            else:
                os.mkdir(path + './修复数据') 
                data.to_csv(outpath,
                        sep=',', index=False, header=True, encoding='ANSI')
    msg_box = QMessageBox(QMessageBox.Information, '处理结束', '日志处理已完成')
    msg_box.exec_()


# ================窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
