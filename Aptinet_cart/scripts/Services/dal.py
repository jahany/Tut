from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, Property
from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel
from Models.product import Product


class DAL():

    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("/home/kast/KAST.db")
        self.CreateTables()

        # print("DataBase Init")
        super().__init__()

    def Connect(self):
        """
        Connect to local DB
        """
        if (self.db.isOpen() == False):
            if (self.db.open() == False):
                print("Error: connection with database failed")
            else:
                # qDebug("Connected To Database")
                pass
        else:
            print("DataBase is Connected")

    def Disconnect(self):
        """
        Disconnect from local DB
        """
        self.db.close()
        print("DataBase DisConnected")

    def CreateTables(self):
        self.Connect()
        query = QSqlQuery()
        if not query.exec_(
            "Create table IF NOT EXISTS Admins ("
            "ID	TEXT NOT NULL UNIQUE,"
            "name TEXT,"
            "isSA INTEGER,"
            "PRIMARY KEY(ID)"
            ")"
        ):
            print("Failed to create table Admin")
        if not query.exec_(
            "CREATE TABLE IF NOT EXISTS Products ("
            "Barcode INTEGER NOT NULL UNIQUE,"
            "name TEXT,"
            "Price INTEGER DEFAULT 0,"
            "FinalPrice INTEGER DEFAULT 0,"
            "UnitCount INTEGER DEFAULT 0,"
            "NotValid INTEGER DEFAULT 0,"
            "PRIMARY KEY(Barcode)"
            ")"
        ):
            print("Failed to create table Products")
        if not query.exec_(
            "CREATE TABLE IF NOT EXISTS ProductsFeatures ("
            "Barcode INTEGER NOT NULL UNIQUE,"
            "w1 INTEGER DEFAULT 0,"
            "w2 INTEGER DEFAULT 0,"
            "w3 INTEGER DEFAULT 0,"
            "w4 INTEGER DEFAULT 0,"
            "w5 INTEGER DEFAULT 0,"
            "w6 INTEGER DEFAULT 0,"
            "w7 INTEGER DEFAULT 0,"
            "w8 INTEGER DEFAULT 0,"
            "w9 INTEGER DEFAULT 0,"
            "w1 INTEGER DEFAULT 0,"
            "IranCode TEXT,"
            "mean INTEGER DEFAULT 0,"
            "tolerance INTEGER DEFAULT 0,"
            "InsertedWeight INTEGER DEFAULT 0,"
            "FOREIGN KEY(Barcode) REFERENCES ProductsFeatures(Barcode)"
            ")"
        ):
            print("Failed to create table ProductsFeatures")
        if not query.exec_(
            "CREATE TABLE IF NOT EXISTS user ("
            "id INTEGER NOT NULL,"
            "Regdate TEXT,"
            "RegTime TEXT,"
            "factorID TEXT,"
            "suspendFactorID TEXT,"
            "Rate INTEGER,"
            "PRIMARY KEY(id)"
            ")"
        ):
            print("Failed to create table user")
        if not query.exec_(
            "CREATE TABLE IF NOT EXISTS userFactor ("
            "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            "uid INTEGER,"
            "Barcode TEXT,"
            "Counter INTEGER,"
            "Price INTEGER,"
            "FinalPrice INTEGER,"
            "FOREIGN KEY(uid) REFERENCES user(id)"
            ")"
        ):
            print("Faild to create table userFactor")
        if not query.exec_(
            "CREATE TABLE IF NOT EXISTS userLog ("
            "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            "weightchanged INTEGER,"
            "barcode TEXT,"
            "state INTEGER,"
            "uid INTEGER NOT NULL,"
            "RegTime TEXT,"
            "adminBarcode TEXT,"
            "FOREIGN KEY(uid) REFERENCES user(id)"
            ")"
        ):
            print("Failed to create TABLE userLog")
