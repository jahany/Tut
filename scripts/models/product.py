from PySide2.QtCore import Qt, QThread, Signal, QObject, Property, Slot
from database.db import DatabaseManager
from scripts.service.scanner import Scanner
import time
import json


class ProductInfo(QObject):
    _name: str = ""
    _barcode: str = ""
    
    @Signal
    def changed():
        pass
    
    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseManager(db_file="database/data.db")
    
    def get_name(self):
        return self._name
    
    def set_name(self, value: str) -> str:
        self._name = value
        print(self._name)
        self.changed.emit()
        
    productname = Property(str, get_name, set_name, notify = changed)
    
    def get_barcode(self):
        return self._barcode
    
    def set_barcode(self, value: str) -> str:
        self._barcode = value
        print(self._barcode)
        self.changed.emit()
        
    product_barcode = Property(str, get_barcode, set_barcode,notify = changed)
    
    
    def get_product_by_qr(self):
        # self.db.store_api_data()
        self.set_barcode(self.db.get_product_barcode(self.get_barcode()))
        print(self._barcode)
        # self.set_name(self.db.get_product_name(self.get_barcode()))    
        # print(self._name)
