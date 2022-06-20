import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


f = open('C:\\output\\test.log', 'rb')
f.seek(0, os.SEEK_END)  # 将流位置改为末尾
last_position = f.tell()  # 上次的流末尾位置
f.close()


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=['*.log'], ignore_patterns=None, ignore_directories=False, case_sensitive=False):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)

    def on_modified(self, event):
        global last_position
        f = open(event.src_path, 'rb')
        f.seek(0, os.SEEK_END)
        now_position = f.tell()
        if now_position == last_position:
            return
        read_bytes = now_position - last_position  # 新增内容
        f.seek(last_position, os.SEEK_SET)  # 光标从开头移动
        data = f.read(read_bytes).decode('utf-8')
        last_position = now_position
        f.close()
        print(data)
        timenow = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        with open('D:\\ICLOG\\all.log','a',newline='') as f:
            for line in data:
                f.write(timenow + '/' + line)
            
            
if __name__ == '__main__':
    print('正在监控')
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='C:\\output', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
