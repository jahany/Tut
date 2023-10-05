from urllib.request import urlopen

from PySide2.QtCore import QThread, Signal,Slot,QEventLoop
from PySide2 import QtCore, QtGui, QtNetwork
from PySide2.QtCore import QByteArray,QFile,QIODevice
from PySide2.QtNetwork import QHttpMultiPart,QHttpPart,QNetworkRequest,QNetworkReply

class Uploader(QThread):

    setCurrentProgress = Signal(int,arguments=["v"])
    succeeded = Signal()

    @Slot(QNetworkReply)
    def UploadFinished(self,reply:QNetworkReply):
        self.succeeded.emit()

    @Slot(int,int)
    def progressbar(self,a:int,b:int):
        if(a > 0 and b > 0):
            print(int((float(a)/float(b))*100.0))
            self.setCurrentProgress.emit(int((float(a)/float(b))*100.0))
        else:
            pass


    def __init__(self):
        super().__init__()
        
    def run(self):
        url = 'http://basket.mykast.ir/Products/UploadFile/upload-file'
        multiPart = QHttpMultiPart(QHttpMultiPart.FormDataType)
        filePart = QHttpPart()
        file =  QFile("/home/kast/KAST.db")
        file.open(QIODevice.ReadOnly)
        print(file.size())
        basketName = ""
        with open("/home/kast/basketName.txt", 'r') as f:
            basketName = str(f.readline())
            basketName = basketName[:-1] + ".db"
            # print(basketName)

        filePart.setHeader(QNetworkRequest.ContentTypeHeader, "application/database")
        filePart.setHeader(QNetworkRequest.ContentDispositionHeader, "form-data; name=\"file\";filename=\"" + basketName + "\"")
        filePart.setHeader(QNetworkRequest.ContentLengthHeader, file.size())

        filePart.setBodyDevice(file)
        multiPart.append(filePart)

        loop = QEventLoop()
        manager = QtNetwork.QNetworkAccessManager()
        manager.finished.connect(self.UploadFinished)
        manager.finished.connect(loop.quit)
        req = QNetworkRequest(url)
        rep = manager.post(req,multiPart)
        multiPart.setParent(rep)
        rep.uploadProgress.connect(self.progressbar)
        loop.exec_()
        #print("exitted")