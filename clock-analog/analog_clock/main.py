import sys
from PySide2.QtCore import Qt, QThread, QCoreApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

from scripts.clock import AnalogClock 



if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    qmlRegisterType(AnalogClock, "analog.binding", 1, 0, "AnalogClock")
    
    engine = QQmlApplicationEngine()


    ctx = engine.rootContext()
    qml_file = "views/analog_clock.qml"
    analog_clock = AnalogClock()
    analog_clock.start()
    # thread = QThread()
    # analog_clock.moveToThread(thread)
    # thread.started.connect(analog_clock.run)
    # thread.start()
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
