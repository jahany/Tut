import RPi.GPIO as GPIO
from PySide2.QtCore import QObject, QThread, Slot,Signal
import time
import numpy as np


class GpioWorker(QThread):
    run:bool= True

    def finishRun(self):
        self.run = False

    def __init__(self,active:bool):
        QThread.__init__(self)
        self.act = active
        
    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(5, GPIO.OUT)
        if(self.act == True):
            GPIO.output(5, GPIO.HIGH)
        else:
            GPIO.output(5, GPIO.LOW)



class L_Wire(QThread):
    def __init__(self, interaction: int):
        QThread.__init__(self)
        # print("\n>>>>>>>>>>>>>>>>>>>>>>>>>lwire thread initialized<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self._interaction = interaction
        self.insert = [0.5, 0.25, 0.5]  # insert -> 1
        self.acceptableBarcodeForDelete = [0.5]  # acceptableBarcodeForDelete -> 2
        self.error = [0.25, 0.15, 0.25]  # error -> 3
        self.deleteHoleList = [0.25, 0.15, 0.25, 0.15, 0.25]  # deleteHoleList -> 4
        self.bypassAccept = [0.5, 0.25, 0.5, 0.25, 0.5]  # bypassAccept -> 5

    def setInteraction(self, val: int):
        self._interaction = val

    def getIntraction(self):
        return self._interaction

    def play(self, pattern: [float]):
        # pass
        on = False
        for t in pattern:
            if on:
                on = False
                GPIO.output(6, GPIO.LOW)
                time.sleep(t)
            if not on:
                on = True
                GPIO.output(6, GPIO.HIGH)
                time.sleep(t)
        GPIO.output(6, GPIO.LOW)
        self.setInteraction(0)  # stable -> 0
        time.sleep(0.1)

    def run(self) -> None:
        GPIO.setwarnings(False)
        GPIO.setup(6, GPIO.OUT)
        if self._interaction == 1:
            self.play(self.insert)
        elif self._interaction == 2:
            self.play(self.acceptableBarcodeForDelete)
        elif self._interaction == 3:
            self.play(self.error)
        elif self._interaction == 4:
            self.play(self.deleteHoleList)
        elif self._interaction == 5:
            self.play(self.bypassAccept)

