from requests import get, Response
from requests.exceptions import HTTPError
import json
from PySide2.QtCore import Signal, Slot, QObject, Property, QTimer, QThread


class GetTimeOnline(QThread):

    _response: Response
    _statuscode: int
    _content: str
    _date: str
    _gmttime: str
    _hour: int = 0
    _minute: int = 0
    _seconds: int = 0

    @Signal
    def changed(self):
        pass

    def getHour(self):
        return self._hour

    def setHour(self, val):
        self._hour = val
        self.changed.emit()

    hourProperty = Property(int, getHour, setHour, notify=changed)

    def getMinutes(self):
        return self._minute

    def setMinutes(self, val):
        self._minute = val
        self.changed.emit()

    minutesProperty = Property(int, getMinutes, setMinutes, notify=changed)

    def getSeconds(self):
        return self._seconds

    def setSeconds(self, val):
        self._seconds = val
        self.changed.emit()

    secondsProperty = Property(int, getSeconds, setSeconds, notify=changed)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.Iran_time)
        self.timer.start(1000)

    def run(self):
        # override
        while 1:
            self.Iran_time()
            print(self.Iran_time())

    @Slot(int)
    def get_time(self):
        try:
            self._response = get(url="https://basket.irannk.com/Basket/getDateTime",
                                 headers={"Content-Type": "application/json"},
                                 params={'q': 'requests+language:python'})
            self._statuscode = self._response.status_code

            if self._statuscode == 200:
                self._content = self._response.content.decode()
                self._date = self._content.split(" ")[0]
                self._gmttime = self._content.split(" ")[1]
                return self._gmttime

            else:
                print("Not Found!")
            if KeyboardInterrupt:
                pass

        except HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f"An error occured: {e}")

    def time_to_seconds(self, stringtime):
        hour, minute, second = map(int, stringtime.split(":"))
        return hour * 60 * 60 + minute * 60 + second

    def seconds_to_time(self,timeseconds):
        """Turn seconds into hh:mm:ss"""
        self._hour = timeseconds // (60 * 60)
        self.setHour(self._hour)
        timeseconds %= (60 * 60) * self._hour
        self._minute = timeseconds // 60
        self.setMinutes(self._minute)
        timeseconds %= 60 * self._minute
        self._seconds = timeseconds
        self.setSeconds(self._seconds)
        return "%02d:%02d:%02d" % (self._hour, self._minute, self._seconds)

    def Iran_time(self):
        gmt_time = self.get_time()
        return self.seconds_to_time(self.time_to_seconds(gmt_time) + self.time_to_seconds("03:30:00"))
