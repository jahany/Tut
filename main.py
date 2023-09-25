import time
import serial
from logic import Logic
from scripts.service.scanner import Scanner
from scripts.models.product import ProductInfo
from database.db import DatabaseManager
import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType,QQmlDebuggingEnabler

from PySide2.QtCore import Qt, QThread, Signal, Slot, QObject, Property


                       
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    qmlRegisterType(Logic, "logic.binding", 1, 0, "Logic")
    
    engine = QQmlApplicationEngine()


    ctx = engine.rootContext()
    qml_file = "views/scanner.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())