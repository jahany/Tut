from PySide2.QtCore import Qt, QThread, Signal, QObject, Property
import requests
import sqlite3
import json


class DatabaseManager(QObject):
    def __init__(self, db_file: str) -> None:
        self.db_file = "database/data.db"
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
    
    def create_product_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS product (
                serial_number VARCHAR PRIMARY KEY
            )'''
        )
        self.connection.commit()
    
    def get_product_barcode(self, serial_number):
        self.cursor.execute('SELECT serial_number FROM product WHERE serial_number = ?', (serial_number,))
        result =  self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return "Product Not found."
        
    def store_api_data(self):
        api_url = "https://basket.irannk.com/Products/GetData"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                self.create_product_table()
                for item in data:
                    serial_number = item.get("Barcode")
                    if serial_number:
                        self.cursor.execute('''
                            INSERT INTO product (serial_number) VALUES (?)''',
                            (serial_number,)
                    )
                        self.connection.commit()
                        print(f"Stored product with serial number {serial_number} in the database.")
            else:
                print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")

            
    