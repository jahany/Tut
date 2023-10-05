from PySide2.QtCore import Signal,Slot,QThread
from Repositories.productRepository import ProductRepository
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel
from Models.product import Product
import os




class SpecialOfferWorker(QThread):

    get = Signal(list, arguments=["v"])

    def __init__(self,rep:ProductRepository):
        QThread.__init__(self)
        self.db1 = QSqlDatabase.addDatabase("QSQLITE","test")
        self.db1.setDatabaseName("/home/kast/KAST.db")
        self.db1.open()
        

    def GetSpecialOffer(self):
        self.query = QSqlQuery(self.db1)
        self.query.exec_("select  *,cast(FinalPrice as Real)/ cast(Price as real) from Products where cast(FinalPrice as Real)/ cast(Price as real) != 1 order by cast(FinalPrice as Real)/ cast(Price as real) asc ")
        res:[Product] = [] 
        while self.query.next():
            p = Product()
            p.setID(self.query.value(0))
            p.setname(self.query.value(1))
            p.setprice(self.query.value(2))
            p.setpic(self.query.value(3))
            p.setfinalprice(self.query.value(4))
            p.setW1(self.query.value(6))
            p.setW2(self.query.value(7))
            p.setW3(self.query.value(8))
            p.setW4(self.query.value(9))
            p.setW5(self.query.value(10))
            p.setW6(self.query.value(11))
            p.setW7(self.query.value(12))
            p.setW8(self.query.value(13))
            p.setW9(self.query.value(14))
            p.setW10(self.query.value(15))
            p.setIrancode(self.query.value(16))
            p.setQRCode(self.query.value(5))
            if (os.path.isfile("/home/kast/pics/" + self.query.value(5) + ".png") == True):
                res.append(p)
                if(len(res)>=12):
                    break
        return res

    def run(self) -> None:
        self.get.emit(self.GetSpecialOffer())

