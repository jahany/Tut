from PySide2.QtCore import QUrl,QObject, Signal, Slot, QByteArray,QEventLoop
import PySide2.QtNetwork 
from PySide2.QtNetwork import QNetworkReply,QNetworkRequest,QNetworkAccessManager
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine,qmlRegisterType
import requests



class restAPI(QObject):

    def __init__(self):
        super().__init__()

    def Get(self, Url:str):
        req = requests.get(Url)
        self.recived.emit(req.text)
        # request = QNetworkRequest(QUrl(Url))
        # # request.setUrl(QUrl(Url))
        # request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,'application/json')
        # restclient = QNetworkAccessManager(self)
        # reply:QNetworkReply= restclient.get(request)
        # reply.waitForReadyRead(5000)
        # print(reply.readAll())
        # restclient.finished.connect(self.replyFinished)

    def Post(self, Url:str, Data):
        headers = {'Content-Type' : 'application/json'}
        rest = requests.post(Url,data=Data,headers=headers)
        self.recived.emit(rest.text)

    recived = Signal(str)

    @Slot(QNetworkReply)
    def replyFinished(self,reply:QNetworkReply):
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        # print("statuscode : " + str(status_code))
        self.recived.emit(str(reply.readAll()))
        print(str(reply.readAll()))



# if __name__ == "__main__":
#     # os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
#     app = QGuiApplication(sys.argv)

#     api =  restAPI()
#     api.Get("http://basket.mykast.ir/Products/GetData") 


#     engine = QQmlApplicationEngine()
#     ctx = engine.rootContext()
#     engine.load("../main.qml")
#     if not engine.rootObjects():
#         sys.exit(-1)
#     sys.exit(app.exec_())
