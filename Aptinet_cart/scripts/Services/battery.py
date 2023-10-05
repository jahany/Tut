import quick2wire.i2c as i2c
from PySide2.QtCore import QObject, Signal, Property, Slot, QUrl, QThread
import numpy as np
from statistics import mean

import time


class BatteryWorker(QThread):
    updateLevel = Signal(int)
    buffer = []
    size = 5
    meanbuffer = []
    meansize = 5
    level: int = 100
    in_init: bool = True

    def __init__(self):
        QThread.__init__(self)
        for i in range(self.size):
            self.buffer.append(0)
        for i in range(self.meansize):
            self.meanbuffer.append(0)

    def run(self):
        try:
            counter = 0
            with i2c.I2CMaster() as bus:
                while True:
                    results = bus.transaction(i2c.reading(0x48, 2))
                    hight = results[0][0]
                    low = results[0][1]

                    data = hight * 256
                    data = data + low
                    self.buffer.pop(0)
                    self.buffer.append(data)
                    res = self.outlierRemover(self.buffer)
                    self.meanbuffer.pop(0)
                    self.meanbuffer.append(res)
                    if (mean(self.meanbuffer) <= 0 or counter <= 10):
                        counter = counter + 1
                        # print(counter)
                        # continue
                    else:
                        Minfile = open("/home/kast/min.txt", "r")
                        mindata = int(Minfile.readline())
                        Minfile.close()

                        if mean(self.meanbuffer) < mindata:
                            Minfile = open("/home/kast/min.txt", "w")
                            Minfile.write(str(int(mean(self.meanbuffer))))
                            Minfile.close()

                        Maxfile = open("/home/kast/max.txt", "r")
                        maxdata = int(Maxfile.readline())
                        Maxfile.close()
                        if mean(self.meanbuffer) > maxdata:
                            Maxfile = open("/home/kast/max.txt", "w")
                            Maxfile.write(str(int(mean(self.meanbuffer))))
                            Maxfile.close()

                        if self.in_init:
                            # if (mean(self.meanbuffer) != 0):
                            self.in_init = False
                            self.level = int(round((mean(self.meanbuffer) - mindata) * 100 / (maxdata - mindata)))
                        else:

                            # print(str(mindata) + ">>>>" + str(maxdata) + ">>>>>>>" + str(mean(self.meanbuffer)))
                            # if (mean(self.meanbuffer) != 0):
                            new_level = int(round((mean(self.meanbuffer) - mindata) * 100 / (maxdata - mindata)))
                            if new_level == (self.level - 1):
                                self.level = new_level
                                self.updateLevel.emit(self.level)
                            elif new_level < (self.level - 1):
                                self.level = self.level - 1
                                self.updateLevel.emit(self.level)
                            elif new_level > (self.level + 4):
                                self.level = self.level + 1
                                self.updateLevel.emit(self.level)
                            # self.level = int(round((mean(self.meanbuffer) - mindata) * 100 / (maxdata - mindata)))
                            # self.updateLevel.emit(self.level)

                        # print(data)
                        # voltage = data * 2.048
                        # voltage = voltage / 32768.0
                        # print(voltage)
                        # self.updateLevel.emit(voltage)
                        if self.level > 100:
                            self.level = 100
                        self.updateLevel.emit(self.level)
                    time.sleep(0.1)
        except:
            pass

    def outlierRemover(self, data_list, outlier_margin=1.5):
        a = np.array(data_list)
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)
        IQR = (upper_quartile - lower_quartile) * outlier_margin
        quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
        resultList = []
        for raw_number in a.tolist():
            if quartileSet[0] <= raw_number <= quartileSet[1]:
                resultList.append(raw_number)
        # print(resultList)
        return int(sum(resultList) / len(resultList)) if len(resultList) > 0 else 0


class Battery(QObject):
    _level: float = 50
    _threadUpdate: BatteryWorker

    def __init__(self):
        super().__init__()
        self._threadUpdate = BatteryWorker()
        self._threadUpdate.updateLevel.connect(self.updateLevel)
        self._threadUpdate.start()

    @Slot(int)
    def updateLevel(self, v: int):
        self.setLevel(v)

    @Signal
    def changed(self):
        pass

    def getLevel(self):
        return self._level

    def setLevel(self, v):
        self._level = v
        self.changed.emit()

    batterylevel = Property(float, getLevel, setLevel, notify=changed)
