# import serial
# from serial import Serial,SerialException
# from PySide2.QtCore import QObject, Slot, Signal,QUrl,QThread, Property
# from threading import Thread
# import time
#
#
# class QRScanner(QObject):
#
#     _qr: str = ""
#     _quantity: int = 0
#     serial_connection = None
#
#     @Signal
#     def changed(self):
#         pass
#
#     #  Getter for QR Code's Value
#     def getQRCode(self):
#         return self._qr
#
#     #   Setter for QR Code's Value
#     def setQRCode(self, value):
#         self._qr = value
#         self.changed.emit()
#
#     #   Property for changing QR Code's value
#     QRCodeProperty = Property(str, getQRCode, setQRCode, notify=changed)
#
#     #  Getter for Quantity
#     def getQuantity(self):
#         return self._quantity
#
#     #   Setter for QR Code's Value
#     def setQuantity(self, value):
#         self._quantity = value
#         self.changed.emit()
#
#     #   Property for changing QR Code's value
#     QuantityProperty = Property(str, getQuantity, setQuantity, notify=changed)
#
#     def __init__(self):
#         super().__init__()
#         th = Thread(target=self.run)
#         th.start()
#
#     def run(self):
#         # self.qr_open()
#         self.qr_read()
#
#     #   Funtion to open the serial port
#
#     def qr_open(self, port="/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS,
#                      parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
#         try:
#             self.serial_connection = Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity,
#                                             stopbits=stopbits, timeout=timeout)
#             return True
#
#         except SerialException as error:
#             print(f"Error while opening the port: {error}")
#
#     #   Funtion to read the data via serial port
#
#     def qr_read(self):
#         if self.qr_open():
#             while True:
#                 try:
#                     time.sleep(5)
#                     # self._qr = "6266841600029"
#                     self._qr = self.serial_connection.read(20)
#                     print("The QR Code is:   ", self._qr)
#                     time.sleep(1)
#                     self._qr = self._qr.decode('utf-8').strip('\r')
#                     data_length = len(self._qr)
#                     if data_length != 0:
#                         print(f"The reading data is {self._qr} and its type is {type(self._qr)}")
#                     self.setQRCode(self._qr)
#                     self._quantity =+ self._quantity
#                     self.setQuantity(self._quantity)
#                     print("This is the QR Code from qr_read() method: ", self._qr)
#                     return self._qr
#
#                 except SerialException as error:
#                     print(f"Error while reading data: {error}")
#
#     #   Function to close the serial port
#
#     def qr_close(self):
#         if self.serial_connection:
#             self.serial_connection.close()
#             print("The serial port is closed")






import serial
from serial import Serial,SerialException
from PySide2.QtCore import QObject, Slot, Signal,QUrl,QThread, Property
from threading import Thread
import time


class QRScanner(QObject):

    _qr: str = ""
    _quantity: int = 0
    serial_connection = None

    @Signal
    def changed(self):
        pass

    #  Getter for QR Code's Value
    def getQRCode(self):
        return self._qr

    #   Setter for QR Code's Value
    def setQRCode(self, value):
        self._qr = value
        self.changed.emit()

    #   Property for changing QR Code's value
    QRCodeProperty = Property(str, getQRCode, setQRCode, notify=changed)

    #  Getter for Quantity
    def getQuantity(self):
        return self._quantity

    #   Setter for QR Code's Value
    def setQuantity(self, value):
        self._quantity = value
        self.changed.emit()

    #   Property for changing QR Code's value
    QuantityProperty = Property(str, getQuantity, setQuantity, notify=changed)

    def __init__(self):
        super().__init__()
        th = Thread(target=self.run)
        th.start()

    def run(self):
        # self.qr_open()
        while True:
            self.qr_read()

    #   Funtion to open the serial port

    def qr_open(self, port="/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS,
                     parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1):
        try:
            self.serial_connection = Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity,
                                            stopbits=stopbits, timeout=timeout)
            return True

        except SerialException as error:
            print(f"Error while opening the port: {error}")

    #   Funtion to read the data via serial port

    def qr_read(self):
        if self.qr_open():
            try:
                # time.sleep(5)
                # self._qr = "6266841600029"
                self._qr = self.serial_connection.read(20)
                time.sleep(1)
                self._qr = self._qr.decode('utf-8').strip('\r')
                data_length = len(self._qr)
                if data_length == 13:
                    print(f"The reading data is {self._qr} and its type is {type(self._qr)}")
                    self.setQRCode(self._qr)
                    self._quantity =+ self._quantity
                    self.setQuantity(self._quantity)
                    print("This is the QR Code from qr_read() method: ", self._qr)
                    return self._qr

            except SerialException as error:
                print(f"Error while reading data: {error}")

    #   Function to close the serial port

    def qr_close(self):
        if self.serial_connection:
            self.serial_connection.close()
            print("The serial port is closed")






