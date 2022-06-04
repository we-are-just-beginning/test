import PySimpleGUI as sg
import pandas as pd
import os


def btnData(path):
    filenames = os.listdir(path)
    file_list = []
    for filename in filenames:
        file_type = filename.split('.')[-1]
        if file_type == 'log':
            file_list.append(filename)
    for file in file_list:
        df = pd.read_csv(path+'/'+file, sep='/', names=['ICCID', 'SEID', 'UID', '打印项'], header=None,
                     dtype=object, encoding='utf-8')  # 读取mca数据成DataFrame
        df.dropna()  # 删除全部空行
        df = df.reset_index(drop=True)  # 重置索引
        df.insert(loc=0, column='OLDICCID', value=df['ICCID']) #插入OLDICCID列
        df2 = df['打印项'].str.split(',', expand=True)  # 按逗号拆分
        df2.rename(columns={0: '打印数据1', 1: '打印数据2', 2: '打印数据3', 3: '打印数据4'}, inplace=True) #打印项重命名
        df2.drop(columns=4, inplace=True)  # 删除原来的打印项
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

sg.theme('Light Blue 2')
layout = [[sg.Text('输入文件路径或选择文件', size=(45, 2), font=20, expand_x=True)],
          [sg.Text('文件路径', size=(8, 1), font=20), sg.Input(key='-IN-', size=(40, 1), font=14),
           sg.FolderBrowse(size=(8, 2), font=16)],
          [sg.Button('处理', size=(15, 2), font=16, expand_x=True, expand_y=True),
           sg.Button('退出', size=(15, 2), font=16, expand_x=True, expand_y=True)]]
window = sg.Window('日志处理', layout, size=(500, 150), element_justification='center')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '退出':
        break
    if event == '处理':
        text_input = values['-IN-']
        btnData(text_input)
    sg.popup_ok('处理完成!')
window.close()
