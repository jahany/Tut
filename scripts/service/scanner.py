from PySide2.QtCore import Qt, QThread, Signal, QObject, Property
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QGuiApplication
from database.db import DatabaseManager
from threading import Thread
import sqlite3
import serial
import json
import time
import sys



class Scanner(QObject):
    _read_bytes: str = ""
    _ser: serial
    
    @Signal
    def qr_read():
        pass
    
    def __init__(
        self,
        urt_port = "/dev/ttyS0",
        baud_rate: int = 9600,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        timeout = 1,
        ) -> None:
        
        super().__init__()
        self._ser = serial.Serial(
                "/dev/ttyS0",
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
        thread = Thread(target=self.run)
        thread.start()   
    
    def get_read_bytes(self):
        return self._read_bytes
        
    def set_read_bytes(self, value: str):
        self._read_bytes = value
        self.qr_read.emit()
        
    qr_code = Property(str, get_read_bytes, set_read_bytes, notify = qr_read)

    def read(self) -> str:
        self._read_bytes = self._ser.readline().decode().strip()
        if len(self._read_bytes) == 13:
            self.set_read_bytes(self._read_bytes)
            return self._read_bytes
        
    def run(self):
        while True:
            self.read()
                    
    def close(self) -> None:
        if self.serial_connection:
            self.serial_connection.close()
            print(f"Serial port {self.urt_port} closed .")
        if self.connection:
            self.connection.close()
            print(f"Sqlite database is closed .")
                    
                    
    

                