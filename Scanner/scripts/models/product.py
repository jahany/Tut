from PySide2.QtCore import QObject, Signal, Property
from scripts.repository.database import Database


class Product(QObject):
    _productQRCode: str = ""
    _productName: str = ""
    _productQuantity: str = ""
    _productPhoto: str = ""
    _productPrice: str = ""
    _productFinalPrice: str = ""

    #   A Signal to notify that anything is changed!
    @Signal
    def changed(self):
        pass

    #   Setter for Product's Name
    def getproductName(self):
        return self._productName

    #   Getter for Product's Name
    def setproductName(self, value):
        self._productName = value
        print("Product name has been set with:  ", value)
        self.changed.emit()

    #   Property for Product's Name
    productNameProperty = Property(str, getproductName, setproductName, notify=changed)

    #   Setter for Product's Photo
    def getproductPhoto(self):
        return self._productPhoto

    #   Getter for Product's Photo
    def setproductPhoto(self, value):
        self._productPhoto = value
        self.changed.emit()

    #   Property for Product's Photo
    productPhotoProperty = Property(str, getproductPhoto, setproductPhoto, notify=changed)

    #   Setter for Product's Price
    def getproductPrice(self):
        return self._productPrice

    #   Getter for Product's Price
    def setproductPrice(self, value):
        self._productPrice = value
        self.changed.emit()

    #   Property for Product's Price
    productPriceProperty = Property(str, getproductPrice, setproductPrice, notify=changed)

    #   Setter for Product's Final Price
    def getproductFinalPrice(self):
        return self._productFinalPrice

    #   Getter for Product's Name
    def setproductFinalPrice(self, value):
        self._productFinalPrice = value
        self.changed.emit()

    #   Property for Product's Name
    productFinalPriceProperty = Property(str, getproductFinalPrice, setproductFinalPrice, notify=changed)

    #  Getter for QR Code's Value
    def getproductQRCode(self):
        return self._productQRCode

    #   Setter for QR Code's Value
    def setproductQRCode(self, value):
        self._productQRCode = value
        self.changed.emit()

    #   Property for changing QR Code's value
    QRCodeProperty = Property(str, getproductQRCode, setproductQRCode, notify=changed)

    #   Setter for Product's Quantity
    def getproductQuantity(self):
        return self._productQuantity

    #   Getter for Product's Name
    def setproductQuantity(self, value):
        self._productQuantity = value
        self.changed.emit()

    #   Property for Product's Name
    productQuantityProperty = Property(str, getproductQuantity, setproductQuantity, notify=changed)

    def get_product_from_db(self, qr):
        # time.sleep(8)
        print("get_product_from_db function starts...")
        self.setproductQRCode(qr)
        print("self._productQRCode is:  ", self._productQRCode, "And self._productName is: ", self._productName)
        pd_name, pd_photo = self.new_db.get_product_by_qr(self.getproductQRCode())
        print("pd_name is: =====>>>>>>", pd_name)
        self.setproductName(pd_name)
        self._productName = pd_name
        print("self._productName is: =====>>>>>>", pd_name)
        print("The product name is:   ", self.getproductName())
        self.setproductPhoto(pd_photo)
        return pd_name

    def add_product_from_db(self, quantity, qr):
        self._productQuantity = self.getproductQuantity()
        print("self._productQuantity is:  ", self._productQuantity)
        self._productQRCode = self.getproductQRCode()
        print("self._productQRCode is:  ", self._productQRCode)
        self.setproductName(input("Enter the Product's Name:   "))
        self._productName = self.getproductName()
        self.setproductPhoto(input("Enter the Product's Photo Path:   "))
        self._productPhoto = self.getproductPhoto()
        self.new_db.add_product(self._productName, self._productPhoto, self._productQuantity, self._productQRCode)
        print(f"A product with name {self._productName} and photo path {self._productPhoto} has been added! ")

    def close_db(self):
        self.new_db.close_db()

    def delete_all_products(self):
        self.new_db.delete_table()
        self.close_db()

    #   Function to initialize
    def __init__(self):
        super().__init__()

    #   Creating an instance of Database to store Product's data
    new_db = Database()
    new_db.connect_db(db="Barcode_Database_3")









