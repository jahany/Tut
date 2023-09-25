from __future__ import annotations
import sqlite3
from sqlite3 import connect, DatabaseError, Error
from PySide2.QtCore import QObject, Slot, Signal, Property
from requests import get, Response
from requests.exceptions import HTTPError
import json
from json import load
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
import os


Base = declarative_base()


class Database(QObject):

    _engine: create_engine
    _session: Session
    _response: Response
    _statuscode: int
    _content: str
    _dbPath: str


    def __init__(self):
        super(Database, self).__init__()
        self._engine = self.create_engine()
        self._session = self.create_session()
        self.createTables()

    def createTables(self):
        Base.metadata.create_all(self._engine)

    def create_session(self):
        return Session(self._engine)

    def create_engine(self):
        try:
            self._dbPath = os.getcwd() + "/data_1.db"
            self._engine = create_engine('sqlite+pysqlite:///' + self._dbPath, echo=True)
            return self._engine.connect()

        except Exception as error:
            print("An error was happened while trying to connect database: \n", error)


    def get_data_from_api(self):
        try:
            self._response = get(url="https://basket.irannk.com/Products/GetData",
                                 headers={"Content-Type": "application/json"},
                                 params={'q': 'requests+language:python'})
            self._statuscode = self._response.status_code
            barcode_list = []
            mean_list = []
            tolerance_list = []
            InsertedWeight_list = []
            Irancode_list = []

            if self._statuscode == 200:
                self._content = self._response.json()
                print("the length of json file is:", len(self._content))
                for item in self._content:
                    barcode_list.append(item["Barcode"])
                    mean_list.append(item["mean"])
                    tolerance_list.append(item["tolerance"])
                    InsertedWeight_list.append(item["InsertedWeight"])
                    Irancode_list.append(item['Irancode'])

                return barcode_list, mean_list, tolerance_list, InsertedWeight_list, Irancode_list

            else:
                print("Not Found!")
            if KeyboardInterrupt:
                pass

        except HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f"An error occured in get_json_data: {e}")

    def insert_data(self, data):
        barcode_list, mean_list, tolerance_list, InsertedWeight_list, Irancode_list = self.get_data_from_api()
        for barcode, mean, tolerance, InsertedWeight, Irancode in \
                zip(barcode_list, mean_list, tolerance_list, InsertedWeight_list, Irancode_list):
            try:
                query = insert(ProductsTable).values(
                    Barcode=barcode,
                    mean=mean,
                    tolerance=tolerance,
                    InsertedWeight=InsertedWeight,
                    Irancode=Irancode
                )
                self._engine.execute(query)
                self._engine.commit()
                # self._newProduct.Barcode = barcode
                # self._newProduct.mean = mean
                # self._newProduct.tolerance = tolerance
                # self._newProduct.InsertedWeight = InsertedWeight
                # self._newProduct.Irancode = Irancode
                # self._session.add(self._newProduct)
                print(f"The product with barcode {ProductsTable.Barcode} has been inserted successfully!")

            except Exception as error:
                print("An error was happened in adding product to the table with error:", error)

    def get_product_by_qr(self, qr_code):
            try:
                query = select(ProductsTable.Irancode, ProductsTable.mean).where(ProductsTable.Barcode == qr_code)
                rows = self._engine.execute(query)
                result = rows.fetchone()
                print("\nresult.....\n", result)
                if result is not None:
                    self._engine.commit()
                    pd_name = result.Irancode
                    pd_photo = result.mean
                    print(f"\n\nName is {pd_name} and QR Code is {qr_code} and the Photo's address {pd_photo}\n\n")
                    return pd_name, pd_photo
                else:
                    return None, None

            except Exception as error:
                print("An error was happened in showing product photo and name with error: \n", error)

    def close_connection(self):
        if self._session:
            self._session.close()


class ProductsTable(Base):

    # Creating a table called Products
    __tablename__ = "Products"

    # Columns of the table Products
    ID = Column(Integer, primary_key=True)
    Barcode = Column(String(20))
    mean = Column(Integer)
    tolerance = Column(Integer)
    InsertedWeight = Column(Integer)
    Irancode = Column(String)

    def __repr__(self):
        return ( f"<Product(Barcode={self.Barcode} , maen={self.mean}, tolerance={self.tolerance}, " \
               f"IntertedWeight={self.InsertedWeight}, Irancode={self.Irancode}" )


#
# class Database(Base):
#
#     # Variable for Database's Name and Database's Cursor
#     _db = SQLDatabase
#     _db_cursor = None
#     _response: Response
#     _statuscode: int
#     _content: str
#     _session: Session
#
#     #   Defining __init__ Function
#     def __init__(self):
#         super().__init__()
#         self._db = SQLDatabase()
#         self._session = self._db.create_session()
#
#     def get_json_data(self):
#         try:
#             self._response = get(url="https://basket.irannk.com/Products/GetData",
#                                  headers={"Content-Type": "application/json"},
#                                  params={'q': 'requests+language:python'})
#             self._statuscode = self._response.status_code
#             barcode = []
#             mean = []
#             tolerance = []
#             InsertedWeight = []
#             Irancode = []
#
#             if self._statuscode == 200:
#                 self._content = self._response.json()
#                 print("the length of json file is:", len(self._content))
#                 for item in self._content:
#                     barcode.append(item["Barcode"])
#                     mean.append(item["mean"])
#                     tolerance.append(item["tolerance"])
#                     InsertedWeight.append(item["InsertedWeight"])
#                     Irancode.append(item['Irancode'])
#
#                 # with open(self._content, 'r') as products_data_json:
#                 #     products_data = load(products_data_json)
#
#                 # barcodes = [item["Barcode"] for item in self._content[:5]]
#                 # products_data = [item for item in self._content[:30]]
#                 # print("Products_data:" , products_data[:30])
#                 return barcode, mean, tolerance, InsertedWeight, Irancode
#
#             else:
#                 print("Not Found!")
#             if KeyboardInterrupt:
#                 pass
#
#         except HTTPError as e:
#             print(f'HTTP error occurred: {e}')
#         except Exception as e:
#             print(f"An error occured in get_json_data: {e}")
#
#     #   Function for connecting to Database
#
#
#     #   Function for creating a table into the database. This table includes
#     #   product's name, product's photo and product's QR Code
#
#     def create_table(self):
#         if self._db_cursor:
#             try:
#                 self._db_cursor.execute("""
#                                     CREATE TABLE IF NOT EXISTS Products
#                                     (
#                                         ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                                         Product_Name varchar(255),
#                                         Product_Photo varchar(255),
#                                         Product_Quantity int,
#                                         Product_QR_code varchar(255)
#                                     )
#                                     """)
#                 self._db.commit()
#                 return True
#
#             except DatabaseError as error:
#                 print("Failed to create a table into the database with error:", error)
#
#     def create_table_from_json(self):
#         if self._db_cursor:
#             try:
#                 self._db_cursor.execute("""
#                                     CREATE TABLE IF NOT EXISTS BarcodesTable
#                                     (
#                                         ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                                         Barcode varchar(255),
#                                         mean int,
#                                         tolerance int,
#                                         InsertedWeight int,
#                                         Irancode varchar(255)
#                                     )
#                                     """)
#                 self._db.commit()
#                 return True
#
#             except DatabaseError as error:
#                 print("Failed to create a table into the database with error:", error)
#
#     def add_product_from_json(self, json_data):
#         barcodes, means, tolerances, InsertedWeights, Irancodes = self.get_json_data()
#         for barcode, mean, tolerance, InsertedWeight, Irancode in zip(barcodes, means, tolerances,
#         InsertedWeights, Irancodes):
#             try:
#                 self._db_cursor.execute("""
#                             INSERT INTO BarcodesTable (ID, Barcode, mean, tolerance, InsertedWeight, Irancode)
#                             VALUES (NULL, ?, ?, ?, ?, ?)
#                             """, (barcode, mean, tolerance, InsertedWeight, Irancode))
#                 self._db.commit()
#                 # self.show_db()
#
#             except DatabaseError as error:
#                 print("An error was happened in adding product to the table with error:", error)
#
#
#     #   Function to show database in Terminal
#
#     def show_db(self):
#         try:
#             self._db_cursor.execute("""
#              SELECT * FROM BarcodesTable
#              """)
#             print(self._db_cursor.fetchall())
#         except Error as error:
#             print("An error was happened in showing database: \n", error)
#
#     #   Funtion to show information of the product by QR Code
#
#     # def get_product_by_qr(self, qr_code):
#     #     if self._db_cursor:
#     #         print("\nget_product_by_qr in Database.....\n")
#     #         try:
#     #             self._db_cursor.execute("""
#     #                         SELECT Product_Name, Product_Photo FROM Products
#     #                         WHERE Product_QR_code = ?
#     #                         """, (qr_code,))
#     #             print("\nqr_code: =====>>>\n", qr_code)
#     #             result = self._db_cursor.fetchone()
#     #             print("\nresult.....\n", result)
#     #             if result is not None:
#     #                 self._db.commit()
#     #                 pd_name = result[0]
#     #                 pd_photo = result[1]
#     #                 print(f"\n\nName is {pd_name} and QR Code is {qr_code} and the Photo's address {pd_photo}\n\n")
#     #                 return pd_name, pd_photo
#     #             else:
#     #                 return None, None
#     #
#     #         except Error as error:
#     #             print("An error was happened in showing product photo and name with error: \n", error)
#
#     #   Function for Adding a Product to the database
#
#     def get_product_by_qr(self, qr_code):
#         if self._db_cursor:
#             print("\nget_product_by_qr in Database.....\n")
#             try:
#                 self._db_cursor.execute("""
#                              SELECT Irancode, mean FROM BarcodesTable
#                              WHERE Barcode = ?
#                              """, (qr_code,))
#                 print("\nqr_code: =====>>>\n", qr_code)
#                 result = self._db_cursor.fetchone()
#                 print("\nresult.....\n", result)
#                 if result is not None:
#                     self._db.commit()
#                     pd_name = result[0]
#                     pd_photo = result[1]
#                     print(f"\n\nName is {pd_name} and QR Code is {qr_code} and the Photo's address {pd_photo}\n\n")
#                     return pd_name, pd_photo
#                 else:
#                     return None, None
#
#             except Error as error:
#                 print("An error was happened in showing product photo and name with error: \n", error)
#
#     def add_product(self, pd_name, pd_photo, pd_qty, pd_qr):
#         try:
#             self._db_cursor.execute("""
#                         INSERT INTO Products (ID, Product_Name, Product_Photo, Product_Quantity, Product_QR_code)
#                         VALUES (NULL, ?, ?, ?, ?)
#                         """, (pd_name, pd_photo, pd_qty, pd_qr))
#             self._db.commit()
#             self.show_db()
#             return pd_name, pd_photo, pd_qty, pd_qr
#
#         except DatabaseError as error:
#             print("An error was happened in adding product to the table with error:", error)
#
#     #   Funtion to delete a product from the table
#
#     def delete_product(self, qr_code):
#         if self.create_table():
#             try:
#                 self._db_cursor.execute("""
#                 DELETE FROM Products
#                 WHERE Product_QR_code = ?
#                 """, qr_code)
#                 self._db.commit()
#
#             except Error as error:
#                 print("An error was happened in deleting product from the table with error:", error)
#
#     #   Funtion to delete the table
#
#     def delete_table(self):
#         if self.create_table():
#             try:
#                 self._db_cursor.execute("""
#                 DROP TABLE IF EXISTS Products
#                 """)
#                 self._db.commit()
#
#             except Error as error:
#                 print("An error was happened in deleting table with error:", error)
#
#     #   Function to close database
#     def close_db(self):
#         self._db.close()
#














