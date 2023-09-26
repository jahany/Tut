import sys
from pathlib import Path

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType
from PySide2.QtCore import QTranslator, QObject, Signal, Slot, Property


class TranslatorController(QObject):
    language: str = ""

    languageChanged = Signal(str)

    def getLanguage(self):
        return self.language

    @Slot(str)
    def setLanguage(self, language):
        self.language = language
        self.languageChanged.emit(self.language)
        print("set language", self.getLanguage())

    languageProperty = Property(str, getLanguage, setLanguage, notify=languageChanged)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    qmlRegisterType(TranslatorController, "akam.binding", 1, 0, "Controller")

    # Load the translation files
    translator_en = QTranslator()
    translator_en.load("translations_en.qm")

    translator_fa = QTranslator()
    translator_fa.load("translations_fa.qm")

    translator_es = QTranslator()
    translator_es.load("translations_es.qm")

#    # Create the translator controller
    translator_controller = TranslatorController()

#    # Connect the languageChanged signal to update the language variable
    language = "en"  # Default language
    translator_controller.languageChanged.connect(lambda lang: setattr(translator_controller, "language", lang))

#    # Set the translator based on the selected language
#    if language == "en":
#    app.installTranslator(translator_en)
#    if language == "fa":
    app.installTranslator(translator_fa)
#    elif language == "es":
#    app.installTranslator(translator_es)

    # Create the QQmlApplicationEngine and set the translator controller as a context property
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("translatorController", translator_controller)

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())




    ## This Python file uses the following encoding: utf-8
    #import sys
    #from pathlib import Path

    #from PySide2.QtGui import QGuiApplication
    #from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
    #from PySide2.QtCore import QTranslator, QObject, Signal, Slot, Property, QThread
    #import time


    #class TranslatorController(QObject):

    #    language: str = ""

    #    languageChanged = Signal(str)

    #    def getLanguage(self):
    #        return self.language

    #    @Slot(str)
    #    def setLanguage(self, language):
    #        self.language = language
    #        self.languageChanged.emit(self.language)
    #        print("set language", self.getLanguage())

    ##    @Slot(str)
    ##    def setLanguage(self, language):
    ##        self.language = language
    ##        self.languageChanged.emit(self.language)
    ##        print("set language", self.getLanguage())

    ##        if self.language == "fa":
    ##            app.installTranslator(translator_fa)
    ##            print("Translator installed: fa")
    ##        elif self.language == "en":
    ##            app.installTranslator(translator_en)
    ##            print("Translator installed: en")
    ##        elif self.language == "es":
    ##            app.installTranslator(translator_es)
    ##            print("Translator installed: es")
    ##        else:
    ##            print("No translator installed")

    #    languageProperty = Property(str, getLanguage, setLanguage, notify=languageChanged)


    #if __name__ == "__main__":
    #    app = QGuiApplication(sys.argv)
    #    qmlRegisterType(TranslatorController, "akam.binding", 1, 0, "Controller")

    #    # Load the translation files
    #    translator_en = QTranslator()
    #    translator_en.load("translations_en.qm")

    #    translator_fa = QTranslator()
    #    translator_fa.load("translations_fa.qm")

    #    translator_es = QTranslator()
    #    translator_es.load("translations_es.qm")

    #    translator_controller = TranslatorController()

    ##    translator_controller.languageChanged.connect(translator_controller.setLanguage(language))
    #    language = "fa"  # Default language
    #    translator_controller.languageChanged.connect(translator_controller.setLanguage)
    #    print("Now the language is:", language)

    ##    if language == "fa":
    #    translator_controller.setLanguage("fa")
    #    app.installTranslator(translator_fa)

    ##    elif language == "es":
    ##        translator_controller.setLanguage("es")
    ##        app.installTranslator(translator_es)

    ##    elif language == "en":
    ##        translator_controller.setLanguage("en")
    ##        app.installTranslator(translator_en)


    #    engine = QQmlApplicationEngine()
    #    engine.rootContext().setContextProperty("translatorController", translator_controller)

    #    qml_file = Path(__file__).resolve().parent / "main.qml"
    #    engine.load(str(qml_file))


    #    if not engine.rootObjects():
    #        sys.exit(-1)

    #    sys.exit(app.exec_())


#import sys
#from pathlib import Path

#from PySide2.QtGui import QGuiApplication
#from PySide2.QtQml import QQmlApplicationEngine
#from PySide2.QtCore import QTranslator


#if __name__ == "__main__":
#    app = QGuiApplication(sys.argv)

#    # Load the translation files
#    translator_en = QTranslator()
#    translator_en.load("translations_en.qm")

#    translator_fa = QTranslator()
#    translator_fa.load("translations_fa.qm")

#    translator_es = QTranslator()
#    translator_es.load("translations_es.qm")

#    # Set the translator based on the selected language
#    language = "en"  # Replace with the appropriate language code based on the button clicked
#    if language == "en":
#        app.installTranslator(translator_en)
#    elif language == "fa":
#        app.installTranslator(translator_fa)
#    elif language == "es":
#        app.installTranslator(translator_es)

#    engine = QQmlApplicationEngine()
#    qml_file = Path(__file__).resolve().parent / "main.qml"
#    engine.load(str(qml_file))
#    if not engine.rootObjects():
#        sys.exit(-1)
#    sys.exit(app.exec_())


#import sys
#from pathlib import Path

#from PySide2.QtGui import QGuiApplication
#from PySide2.QtQml import QQmlApplicationEngine
#from PySide2.QtCore import QTranslator


#if __name__ == "__main__":
#    app = QGuiApplication(sys.argv)

#    # Load the translation files
#    translator_en = QTranslator()
#    translator_en.load("translations_en.qm")

#    translator_fa = QTranslator()
#    translator_fa.load("translations_fa.qm")

#    translator_es = QTranslator()
#    translator_es.load("translations_es.qm")

#    # Set the translator based on the selected language
#    language = "en"  # Replace with the appropriate language code based on the button clicked
#    if language == "en":
#        app.installTranslator(translator_en)
#    elif language == "fa":
#        app.installTranslator(translator_fa)
#    elif language == "es":
#        app.installTranslator(translator_es)

#    engine = QQmlApplicationEngine()
#    qml_file = Path(__file__).resolve().parent / "main.qml"
#    engine.load(str(qml_file))
#    if not engine.rootObjects():
#        sys.exit(-1)
#    sys.exit(app.exec_())
