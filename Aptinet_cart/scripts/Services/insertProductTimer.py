from PySide2.QtCore import QObject, QThread, Slot,Signal


class InsertProductTimerWorker(QThread):
    run:bool= True

    def finishRun(self):
        self.run = False

    def __init__(self):
        QThread.__init__(self)
        
    def run(self):
        pass