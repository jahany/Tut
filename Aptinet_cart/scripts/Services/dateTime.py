from time import sleep
from PySide2.QtCore import qDebug, QObject, Signal, Slot, QThread
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
import sys
from Services.restapi import restAPI


class DateTimeWorker(QThread):
    h: int = 0
    s: int = 0
    m: int = 0
    update = Signal(int, int, int)

    def __init__(self):
        QThread.__init__(self)

    def getDate(self, h: int, m: int, s: int):
        self.h = h
        self.m = m
        self.s = s

    def run(self):
        while True:
            self.s = self.s + 1
            if self.s == 60:
                self.s = 0
                self.m = self.m + 1
            if self.m == 60:
                self.m = 0
                self.h = self.h + 1
            self.update.emit(self.h, self.m, self.s)
            sleep(1)


class DateTime(QObject):
    history: str = ""
    s: int = 0
    m: int = 0
    h: int = 0
    time: str = ""

    def __init__(self) -> None:
        #self.getDateTime()
        print("dateTime Started")
        super().__init__()

    def getDateTime(self):
        rest = restAPI()
        rest.recived.connect(self.dateTimeRecived)
        #rest.Get("http://basket.mykast.ir/Basket/getDateTime")
        #rest.Get("http://10.114.1.10:8080/onlineshop/getservertime")
        # print("dateTime Connected")

    @Slot(str)
    def dateTimeRecived(self, res: str):
        # print("dateTime Resived")
        # print(res)
        arr = res.split(" ")
        self.historyHandler(arr[0])
        self.timeHander(arr[1], arr[2])

    def historyHandler(self, res: str):
        arr = res.split("/")
        if (len(arr[0]) == 1):
            arr[0] = "0" + arr[0]
        if (len(arr[1]) == 1):
            arr[1] = "0" + arr[1]

        self.history = arr[2] + arr[0] + arr[1]

    def timeHander(self, res: str, ap: str):
        arr = res.split(":")
        if (ap == "PM"):
            arr[0] = str(int(arr[0]) + 12)
        self.h = arr[0]
        self.m = arr[1]
        self.s = arr[2]
        self.thread = DateTimeWorker()
        self.thread.update.connect(self.setUpdatedTime)
        self.thread.getDate(int(self.h), int(self.m), int(self.s))
        self.thread.start()
        # thread.deleteLater()

    @Slot(int, int, int)
    def setUpdatedTime(self, hh: int, mm: int, ss: int):
        self.h = hh
        self.m = mm
        self.s = ss
        self.time = str(hh) + ":" + str(mm) + ":" + str(ss)
