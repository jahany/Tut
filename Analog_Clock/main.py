import sys
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType
from scripts.models.logic import GetTimeOnline


if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    qmlRegisterType(GetTimeOnline, "akam.binding", 1, 1, "GetTimeOnline")

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()

    gto = GetTimeOnline()
    gto.start()

    qml_file = "main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
import sys
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType
from scripts.models.logic import GetTimeOnline


if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    qmlRegisterType(GetTimeOnline, "akam.binding", 1, 1, "GetTimeOnline")

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()

    gto = GetTimeOnline("Asia/Tehran")
    gto.start()

    qml_file = "main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
