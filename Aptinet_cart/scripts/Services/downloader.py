from PySide2.QtNetwork import QHttpMultiPart,QHttpPart,QNetworkRequest,QNetworkReply
from PySide2 import QtNetwork
from PySide2.QtCore import QThread, Signal,Slot,QEventLoop,QFile,QIODevice

class Downloader(QThread):

    setCurrentProgress = Signal(int,arguments=["v"])
    succeeded = Signal()

    def __init__(self):
        super().__init__()

    @Slot(int,int)
    def progressbar(self,a:int,b:int):
        if(a > 0 and b > 0):
            print(int((float(a)/float(b))*100.0))
            self.setCurrentProgress.emit(int((float(a)/float(b))*100.0))
        else:
            pass
    
    @Slot(QNetworkReply)
    def downloadFinished(self,reply: QNetworkReply):
        print("start save file")
        dfile = QFile("/home/kast/FinalFASKET/FASKET.zip")
        if dfile.open(QIODevice.WriteOnly):
            dfile.write(reply.readAll())

        dfile.close()
        self.succeeded.emit()
        self.loop.quit()

    def run(self):
        url = "http://irannk.com/FASKET.zip"
        self.loop = QEventLoop()
        manager = QtNetwork.QNetworkAccessManager()
        manager.finished.connect(self.downloadFinished)
        req = QNetworkRequest(url)
        
        rep = manager.get(req)
        rep.downloadProgress.connect(self.progressbar)
       
        self.loop.exec_()
        print("exitted")