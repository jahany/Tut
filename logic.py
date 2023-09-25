from scripts.models.product import ProductInfo
from scripts.service.scanner import Scanner
from database.db import DatabaseManager
from PySide2.QtCore import Qt, QThread, Signal, Slot, QObject, Property
import time
import serial


class Logic(QObject):
    _product : ProductInfo = ""
    
    @Signal
    def changed(self):
        pass
    
    def get_product(self):
        return self._product
    
    def set_product(self, value):
        self._product = value
        self.changed.emit()
        
    read_product = Property(ProductInfo, get_product, set_product, notify=changed)
    
    def __init__(self):
        super().__init__()
        self.scanner = Scanner()
        self._product = ProductInfo()
        self.database = DatabaseManager(db_file="database/data.db")
        self.scanner.qr_read.connect(self.handle_qr_read)
        
    @Slot(str)
    def handle_qr_read(self):
        print(self.scanner.qr_code)
        self._product.set_barcode(self.scanner.get_read_bytes())

        
        
