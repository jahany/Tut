from PySide2.QtCore import QObject, Signal, Property, Slot
from scripts.services.scanner import QRScanner
from scripts.models.product import Product


class Logic(QObject):

    # @Slot
    # def readedbarcode(self):
    #     # self.my_scanner.getQRCode()
    #     # self._Pd.getproductQRCode()
    #     self.my_scanner.setQRCode()
    #     self._Pd.QRCodeProperty()
    #     # self._Pd.get_product_from_db(self.my_scanner.QRCodeProperty)
    #
    # @Slot
    # def readedquantity(self):
    #     self.my_scanner.QuantityProperty()
    #     self._Pd.productQuantityProperty()
    #     # self.my_scanner.getQuantity()
    #     # self._Pd.getproductQRCode()

    _Pd: Product

    @Signal
    def changed(self):
        pass

    def getProduct(self):
        return self._Pd

    def setProduct(self, val):
        self._Pd = val
        self.changed.emit()

    productProperty = Property(Product, getProduct, setProduct, notify=changed)

    @Slot(str)
    def readedbarcode(self):
        self._Pd.setproductQRCode(self.my_scanner.getQRCode())
        self._Pd.setproductName(self._Pd.get_product_from_db(self.my_scanner.getQRCode()))

    def __init__(self):
        super().__init__()
        self._Pd = Product()
        self.my_scanner = QRScanner()
        self.run()

    def run(self):
        self.my_scanner.changed.connect(self.readedbarcode)
            # self._Pd.setproductQRCode(self.my_scanner.getQRCode())

            # my_scanner.changed.connect(.readedbarcode)
            # temp_qr = my_scanner.qr_read()
            # print("This is the qr: ", temp_qr)
            # _Pd.setproductQRCode(temp_qr)
            # _Pd.delete_all_products()
        # time.sleep(8)
        print("self.my_scanner.getQRCode():    ", self.my_scanner.getQRCode())
        self._Pd.get_product_from_db(self.my_scanner.getQRCode())


# while True
    # user_input = input("Add Product [a] or Find Product [f]?")
    # if user_input == 'a':
    #     # self._Pd.setproductQRCode(self.my_scanner.getQRCode())
    #     self._Pd.add_product_from_db(self.my_scanner.getQRCode(), self.my_scanner.getQuantity())
    #     print("Output of my_scanner.getQRCode:  ", self.my_scanner.getQRCode())
    #
    # elif user_input == 'f':
    #     print("You chose f!!!")
    #     # self._Pd.setproductQRCode(self.my_scanner.getQRCode())
    #     self._Pd.get_product_from_db(self.my_scanner.getQRCode())
    #     print("get product has been ended")
    # else:
    #     self._Pd.close_db()
    #     break




