import sys
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType
from logic import Logic


if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    # app.setOverrideCursor(Qt.BlankCursor)
    qmlRegisterType(Logic, "akam.binding", 1, 0, "Logic_Class")

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()
    qml_file = "views/main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())