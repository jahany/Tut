from PySide2.QtCore import QObject, Signal, Property, Slot
from Module.hx711 import HX711
import numpy as np
from threading import Thread
from time import sleep
from statistics import mean



class WeighSensorCalibration(QObject):
    _raw_digit = []
    _raw_wight = []
    _offset : float
    _scale : float
    _w1:int
    _w2:int
    _w3:int

    _readStartWeight: int = 0
    _BasketWeight1: int = 0
    _BasketWeight2: int = 0
    _currentWeight: int = 0
    _telorance: float = 25

    _avgweight:int = 0
    _basketweight = 0
    _canread = False


    noise_reduction_buffer_size = 50
    noise_reduction_buffer = []
    last_weight = 0
    read_weight_buffer_size = 50
    read_weight_buffer = []
    lightest_weight = 8
    acceptable_tolerance = 8
    ignored_bits = 0

    def __init__(self):
        super().__init__()
        self.hx = HX711(23,24)
        for i in range(self.read_weight_buffer_size):
            self.read_weight_buffer.append(0)
        for i in range(self.noise_reduction_buffer_size):
            self.noise_reduction_buffer.append(0)
        thread = Thread(target=self.threaded_function)
        thread.start()
        with open("/home/kast/offset.txt", 'r') as f:
            self.setOffset(float(f.readline()))
        self.hx.set_offset(self._offset)
        with open("/home/kast/scale.txt", 'r') as f:
            self.setScale(float(f.readline()))
        self.hx.set_scale(self.scale)




    @Signal
    def currentweight_changed(self):
        pass

    startWeightchanged = Signal(int)

    @Signal
    def changed(self):
        pass

    def getOffset(self):
        return self._offset

    def setOffset(self, v):
        self._offset = v
        self.changed.emit()

    offset = Property(float,getOffset,setOffset,notify = changed)

    def getScale(self):
        return self._scale

    def setScale(self,v):
        self._scale = v
        self.changed.emit()

    scale = Property(float,getScale,setScale,notify = changed)

    def getcurrentweight(self):
        return self._currentWeight

    def setcurrentweight(self, val):
        self._currentWeight = val
        self.currentweight_changed.emit()

    currentweight = Property(int, getcurrentweight, setcurrentweight, notify=currentweight_changed)

    def getw1(self):
        return self._w1

    def setw1(self, val):
        self._w1 = val
        self.changed.emit()

    w1 = Property(int, getw1, setw1, notify=changed)

    def getw2(self):
        return self._w2

    def setw2(self, val):
        self._w2 = val
        self.changed.emit()

    w2 = Property(int, getw2, setw2, notify=changed)

    def getw3(self):
        return self._w3

    def setw3(self, val):
        self._w3 = val
        self.changed.emit()

    w3 = Property(int, getw3, setw3, notify=changed)

    def outlierRemover(self, data_list, outlier_margin=1.5):
        a = np.array(data_list)
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)
        IQR = max(((upper_quartile - lower_quartile) * outlier_margin),8)
        quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
        resultList = []
        for raw_number in a.tolist():
            if quartileSet[0] <= raw_number <= quartileSet[1]:
                resultList.append(raw_number)
        # print(resultList)
        return int(sum(resultList) / len(resultList)) if len(resultList) > 0 else 0

    def readbasketweight(self):
        return self._basketweight

    def setbasketweight(self, val):
        self._basketweight = val
        self.changed.emit()

    basketweight_changed=Signal(int,int)


    basketweight = Property(int, readbasketweight, setbasketweight, notify=changed)

    def readAvgweight(self):
        return self._avgweight

    def setAvgweight(self, val):
        self._avgweight = val
        self.changed.emit()


    basketAVGweight = Property(int, readAvgweight, setAvgweight, notify=changed)

    def threaded_function(self):
        while True:
            self.ReadWeight()

            sleep(0.01)

    lastcurrentweightLint =0
    def ReadWeight(self):
        result: int = self.hx.get_grams(times=1)

        self.noise_reduction_buffer.pop(0)
        self.noise_reduction_buffer.append(int(result))

        self.setcurrentweight(self.outlierRemover(self.noise_reduction_buffer, 1))

        self.read_weight_buffer.pop(0)
        self.read_weight_buffer.append(self.getcurrentweight())

        self.setAvgweight(mean(self.read_weight_buffer))
        self._canread = True
        for i in range(self.read_weight_buffer_size):
            for j in range(self.read_weight_buffer_size):
                max_difference_read_weight = abs(self.read_weight_buffer[i] - self.read_weight_buffer[j])
                if max_difference_read_weight >= self.acceptable_tolerance:
                    self._canread = False
                    break

        if self._canread:
            self._BasketWeight2 = mean(self.read_weight_buffer)
            if abs(self._BasketWeight2 - self._BasketWeight1) > self.lightest_weight:
                self.basketweight_changed.emit(self._BasketWeight2, self._BasketWeight1)
                self.setbasketweight(int(self._BasketWeight2))

            self._BasketWeight1 = self._BasketWeight2

    @Slot()
    def setWeightZero(self):
        weights = []
        for i in range(24):
            weights.append(self.hx.read())
        self._raw_digit.append(self.outlierRemover(weights))
        self._raw_wight.append(0)

    @Slot(str)
    def setWeightW1(self,v:str):
        self.setw1(v)

        weights = []
        for i in range(24):
            weights.append(self.hx.read())
        self._raw_digit.append(self.outlierRemover(weights))
        self._raw_wight.append(float(v))
        scale, offset = np.polyfit(self._raw_wight, self._raw_digit, 1)
        self.hx.set_offset(offset)
        self.hx.set_scale(scale)
        self.setScale(scale)
        self.setOffset(offset)

    @Slot(str)
    def setWeightW2(self,v:str):
        self.setw2(v)
        weights = []
        for i in range(24):
            weights.append(self.hx.read())
        self._raw_digit.append(self.outlierRemover(weights))
        self._raw_wight.append(float(v))
        scale, offset = np.polyfit(self._raw_wight, self._raw_digit, 1)
        self.hx.set_offset(offset)
        self.hx.set_scale(scale)
        self.setScale(scale)
        self.setOffset(offset)

    @Slot(str)
    def setWeightW3(self,v:str):
        self.setw3(v)
        weights = []
        for i in range(24):
            weights.append(self.hx.read())
        self._raw_digit.append(self.outlierRemover(weights))
        self._raw_wight.append(float(v))
        scale, offset = np.polyfit(self._raw_wight, self._raw_digit, 1)
        self.hx.set_offset(offset)
        self.hx.set_scale(scale)
        self.setScale(scale)
        self.setOffset(offset)

    @Slot()
    def saveCalibration(self):
        # print("fucked")
        with open("/home/kast/offset.txt", 'w') as f:
            f.write(str(self.hx.get_offset()))
        with open("/home/kast/scale.txt", 'w') as f:
            f.write(str(self.hx.get_scale()))

