import sys
import requests
import json
from datetime import datetime
import time
from PyQt6.QtWidgets import *
from PyQt6.Qt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
from Ui_cd import *
import _thread



ClickTime = 0


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'
    }

url = 'https://acs.m.taobao.com/gw/mtop.common.getTimestamp/'

with open('config.json') as file:
        file = file.read()
        sel = json.loads(file)
selWeekday = sel['SetWeekday']

def getreq():
    reqjson = requests.post(url=url, headers=headers)
    req = json.loads(reqjson.text)
    timed = req['data']
    times = timed['t']
    times = float(times)
    times = times / 1000
    wkd = datetime.date(datetime.fromtimestamp(times)).weekday()
    year = time.strftime("%Y", time.localtime(times))
    moonth = time.strftime("%m", time.localtime(times))
    day = time.strftime("%d", time.localtime(times))
    hour = time.strftime("%H", time.localtime(times))
    min = time.strftime("%M", time.localtime(times))
    sec = time.strftime("%S", time.localtime(times))
    return wkd, year, moonth, day, hour, min, sec



def Gettime():
    wkd, year, moonth, day, hour, min, sec = getreq()
    if wkd > selWeekday:
        time = wkd - selWeekday
        time = 7 - time
    elif wkd < selWeekday:
        time = selWeekday - wkd
    else:
        time = 0
    return time, year, moonth, day, hour, min, sec



class Windows(QMainWindow,Ui_Form):
    def __init__(self):
        super(Windows,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clickbtn)




    def clickbtn(self):
        def DoTimeCheck(self):
            time, year, moonth, day, hour, min, sec = Gettime()
            self.lcdNumber.display(time)
            self.lcdNumber_2.display(year)
            self.lcdNumber_3.display(moonth)
            self.lcdNumber_4.display(day)
            self.lcdNumber_7.display(hour)
            self.lcdNumber_5.display(min)
            self.lcdNumber_6.display(sec)
        def loop(self):
            if self.checkBox.isChecked():
                DoTimeCheck(self)
                loop(self)
                time.sleep(0.5)
            else:
                DoTimeCheck(self)
        
        _thread.start_new_thread( loop, (self,))







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Windows()
    window.setWindowTitle("星期倒计时")
    icon = QIcon("icon.ico")
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())