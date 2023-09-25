from PySide2.QtCore import QObject, QTimer, Signal, Property, QThread, QCoreApplication, Slot
from datetime import datetime, timedelta
import requests


class AnalogClock(QThread):
    @Signal
    def time_second_changed(self):
        pass
    
    @Signal
    def time_minute_changed(self):
        pass
    
    @Signal
    def time_hour_changed(self):
        pass
    
    def get_hour(self):
        return self._hour
    
    def set_hour(self, value):
        self._hour = value
        self.time_hour_changed.emit()
        
    read_hour = Property(str, get_hour, set_hour, notify=time_hour_changed)
    
    def get_minute(self):
        return self._minute
    
    def set_minute(self, value):
        self._minute = value
        self.time_minute_changed.emit()  
        
    read_minute = Property(str, get_minute, set_minute, notify=time_minute_changed)
    
    def get_second(self):
        return self._second
    
    def set_second(self, value):
        self._second = value
        self.time_second_changed.emit() 
        
    read_second = Property(str, get_second, set_second, notify=time_second_changed)
         
    def __init__(self):
        super().__init__()
        self._second = ""
        self._hour = ""
        self._minute = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
    @Slot()    
    def update_time(self):        
       try:
            response = requests.get("https://basket.irannk.com/Basket/getDateTime")
            if response.status_code == 200:
                result = response.text
                date, time = result.split() 
                get_time = datetime.strptime(time, "%H:%M:%S") +  timedelta(hours=3, minutes=30)
                self.set_hour(get_time.strftime("%H"))
                self.set_minute(get_time.strftime("%M"))
                self.set_second(get_time.strftime("%S"))
            else:
                print(f"Api failed with status code : {response.status_code} ")
            
       except requests.exceptions.RequestException as e:
           print(f"Error : {e}")
           
    def run(self):
        while True:
            self.update_time()
   

                
        
