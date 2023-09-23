from requests import get, Response
from requests.exceptions import HTTPError
import json
from PySide2.QtCore import Signal, Slot, QObject, Property, QTimer, QThread


class GetTimeOnline(QThread):

    _response: Response
    _statuscode: int
    time_zone: str = 'Asia/Tehran'
    _jsonfile: json
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

    def __init__(self, time_zone: str ='Asia/Tehran'):
        super().__init__()
        self.time_zone = time_zone
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.timer.start(1000)

    def run(self):
        # override
        while 1:
            self.get_time()
    @Slot(int)
    def get_time(self):
        try:
            self._response = get(url=f"https://timeapi.io/api/Time/current/zone?timeZone={self.time_zone}",
                                 headers={"Content-Type":"application/json"},
                                 params={'q': 'requests+language:python'})
            self._statuscode = self._response.status_code

            if self._statuscode == 200:
                self._jsonfile = self._response.json()
                self.setHour(self._jsonfile['hour'])
                self.setMinutes(self._jsonfile['minute'])
                self.setSeconds(self._jsonfile['seconds'])
                print(f"{self._hour} : {self._minute} : {self._seconds}")
                print(self.getSeconds())
                self.secondsProperty

            else:
                print("Not Found!")
            if KeyboardInterrupt:
                pass

        except HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f"An error occured: {e}")


