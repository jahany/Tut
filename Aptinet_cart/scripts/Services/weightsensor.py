from PySide2.QtCore import QObject, Signal, Property, Slot,QThread
from scripts.Module.hx711 import HX711
import numpy as np
from time import sleep
from statistics import mean
from copy import copy


class WeightSensorWorker(QThread):

    _offset: float
    _scale: float
    _startWeight: int = 0 
    _BasketWeight1: int = 0
    _BasketWeight2: int = 0
    _currentWeight: int = 0
    _tolerance: float = 25
    _basketweight = 0
    _canread = False
    _atstartUp = True
    _startUpHandler = 0
    _isStable: bool = False

    noise_reduction_buffer_size = 20
    noise_reduction_buffer = []
    last_weight = 0
    read_weight_buffer_size = 20 # buffer size for shifting weights to it
    read_weight_buffer = [] #buffer for shifting weights to it
    lightest_weight = 25  # 8
    lightest_weight_for_remove = 17  # 25 - 8
    acceptable_tolerance = 8
    ignored_bits = 0
    is_stable_tolerance = 25

    def __init__(self):
        super().__init__()
        self._startUpHandler = self.noise_reduction_buffer_size
        self.hx = HX711(23, 24)
        for i in range(self.read_weight_buffer_size):
            self.read_weight_buffer.append(0)
        for i in range(self.noise_reduction_buffer_size):
            self.noise_reduction_buffer.append(0)
        with open("/home/kast/offset.txt", 'r') as f:
            a = f.readline().strip()
            if a:
                self.setOffset(float(a))
            else:
                print('empty str')
            # self.setOffset(float(f.readline()))
        # self.hx.set_offset(self._offset)
        with open("/home/kast/scale.txt", 'r') as f:
            a = f.readline().strip()
            if a:
                self.setScale(float(a))
            else:
                print('empty str')
            # self.setScale(float(f.readline()))
        # self.hx.set_scale(self.scale)
        self.lightest_weight_register = self.lightest_weight

    @Signal
    def changed(self):
        pass

    @Signal
    def currentweight_changed(self):
        pass

    @Signal
    def isstable_changed(self):
        pass

    def getOffset(self):
        return self._offset

    def setOffset(self, v):
        self._offset = v
        self.changed.emit()

    offset = Property(float, getOffset, setOffset, notify=changed)

    def getScale(self):
        return self._scale

    def setScale(self, v):
        self._scale = v
        self.changed.emit()

    scale = Property(float, getScale, setScale, notify=changed)

    def getcurrentweight(self):
        return self._currentWeight

    def setcurrentweight(self, val):
        self._currentWeight = val
        self.currentweight_changed.emit()

    currentweight = Property(int, getcurrentweight, setcurrentweight, notify=currentweight_changed)

    startWeightchanged = Signal(int)

    def readbasketweight(self):
        return self._basketweight

    def setbasketweight(self, val):
        self._basketweight = val
        self.changed.emit()

    basketweight_changed = Signal(int, int)
    basketweight = Property(int, readbasketweight, setbasketweight, notify=changed)

    def getstartWeight(self):
        return self._startWeight

    def setstartWeight(self, val: int):
        # print("set start weight is " + str(val))
        self._startWeight = val
        self.startWeightchanged.emit(val)

    startWeight = Property(int, getstartWeight, setstartWeight, notify=startWeightchanged)

    def getisstable(self):
        return self._isStable

    def setisstable(self, val):
        self._isStable = val
        self.isstable_changed.emit()

    isstable = Property(bool, getisstable, setisstable, notify=isstable_changed)

    def outlierRemover(self, data_list: list, outlier_margin=1.5):
        # converts data  list into a numpy array
        a = np.array(data_list)
        # calculate upper quartile of numerics. it mean 3/4 data
        upper_quartile = np.percentile(a, 75)
        # calculate upper quartile of numerics. it mean 1/4 data
        lower_quartile = np.percentile(a, 25)
        # calculate measure of the spread of the data
        # it ensure that if calculated value is at least 8 .
        IQR = max(((upper_quartile - lower_quartile) * outlier_margin), 8)
        # calculate period of data and remove outlier data
        quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
        # define empty list
        resultList = []
        # convert numpy array into python list to iterate over it
        # for each number into the list checks 
        for raw_number in a.tolist():
            # if 'raw_number' is greater than the lower bound and less than the upper bound
            # in simple terms it checks if it is inside the range
            if quartileSet[0] <= raw_number <= quartileSet[1]:
                # if condition is True it collect all the numbers that are not outlier
                resultList.append(raw_number)
        # calculate average of data and if lenght of list is less than 0
        # it means there are no values to calculate so it return 0
        return int(sum(resultList) / len(resultList)) if len(resultList) > 0 else 0

    def run(self):
        # it starts infinite loop it means code inside loop keep running
        while True:
            # calling 'get_grams' method and assigning to a 'result' variable
            result: int = self.hx.get_grams(times=1)

            # pop the first element (oldest) from 'noise_reduction_buffer' list
            self.noise_reduction_buffer.pop(0)
            # appends new result to the end of the list
            self.noise_reduction_buffer.append(int(result))

            # update the current weight value 
            self.setcurrentweight(self.outlierRemover(self.noise_reduction_buffer, 1))

            # pop the first element from 'read_weight_buffer' list
            self.read_weight_buffer.pop(0)
            # appends current weight to the end of the weight buffer
            self.read_weight_buffer.append(self.getcurrentweight())
            # if 'startUPHandler' is grater than 0 decrements this value by 1
            if self._startUpHandler > 0:
                self._startUpHandler = self._startUpHandler - 1
            else:
                self.setisstable(True)
                self._canread = True
                for i in range(self.read_weight_buffer_size):
                    for j in range(i, self.read_weight_buffer_size):
                        diff = abs(self.read_weight_buffer[i] - self.read_weight_buffer[j])
                        if diff >= self.is_stable_tolerance:
                            self.setisstable(False)
                            self._canread = False
                            break
                        elif diff >= self.acceptable_tolerance:
                            self._canread = False

                if self._canread:
                    if self._atstartUp == True:
                        # call setstartweight based on the average of weight buffer
                        self.setstartWeight(mean(self.read_weight_buffer))
                        self._BasketWeight2 = mean(self.read_weight_buffer)
                        self._BasketWeight1 = self._BasketWeight2
                        self._atstartUp = False
                    else:
                        if mean(self.read_weight_buffer) > self._BasketWeight1:
                            a = np.array(self.read_weight_buffer)
                            half_quartile = np.percentile(a, 50)
                            c = 0
                            s = 0
                            for w in self.read_weight_buffer:
                                if w >= half_quartile:
                                    c += 1
                                    s += w
                            self._BasketWeight2 = int(s / c)
                        else:
                            self._BasketWeight2 = mean(self.read_weight_buffer)
                        if (self._BasketWeight2 - self._BasketWeight1) >= self.lightest_weight or (
                                self._BasketWeight2 - self._BasketWeight1) <= (
                                -1 * min(self.lightest_weight, self.lightest_weight_for_remove)):
                            self.basketweight_changed.emit(self._BasketWeight2, self._BasketWeight1)
                            self.setbasketweight(int(self._BasketWeight2))
                        
                        self._BasketWeight1 = self._BasketWeight2

    def stopWeightSensorRead(self):
        del self.hx

    # def __del__(self):
    #     print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Weight Sensor Deleted <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
