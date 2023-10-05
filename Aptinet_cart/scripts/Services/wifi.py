import stat
from ast import Dict
import subprocess as sp
import re
import os
from typing import Any
from PySide2.QtCore import QObject, Signal, Property, QAbstractListModel, QModelIndex, Slot, Qt, QByteArray ,QThread
from time import sleep


class Wireless(QObject):
    _essid: str = ""
    _ip: str = ""
    _quality: str = ""
    _signalLevel: str = ""
    _isConnected: bool = False

    def __init__(self):
        super().__init__()

    @Signal
    def changed(self):
        pass

    def getIP(self):
        return self._ip

    def setIP(self, x):
        self._ip = x
        self.changed.emit()

    IP = Property(str, getIP, setIP, notify=changed)

    def getESSID(self):
        return self._essid

    def setESSID(self, x):
        self._essid = x
        self.changed.emit()

    ESSID = Property(str, getESSID, setESSID, notify=changed)

    def getQuality(self):
        return self._quality

    def setQuality(self, x):
        self._quality = x
        self.changed.emit()

    Quality = Property(str, getQuality, setQuality, notify=changed)

    def getSignallevel(self):
        return self._signalLevel

    def setSignallevel(self, x):
        self._signalLevel = x
        self.changed.emit()

    Signallevel = Property(str, getSignallevel, setSignallevel, notify=changed)

    def getIsConnect(self):
        return self._isConnected

    def setIsConnect(self, x):
        self._isConnected = x
        self.changed.emit()

    IsConnected = Property(bool, getIsConnect, setIsConnect, notify=changed)


class ScannerWorker(QThread):
    updateListView = Signal(list)
    updateConnectedWifi = Signal(str,str)
    finished:bool = False
    def __init__(self):
        QThread.__init__(self)
        
    def setFinished(self,res:bool):
        self.finished = res
    def run(self):
        listw = []
        while self.finished == False:
            print("wifi scanned")
            self.allWireless()
            self.connectedWireLess()
            sleep(5)
        
    # show which wireless connecteing and get ip
    def allWireless(self):
        allInfo = sp.getoutput("sudo iwlist wlan0 scan")
        nameOutput = re.findall("ESSID:\"(.*?)\"\n", allInfo)
        quality = re.findall("Quality=(\d+?)/(\d+?)  ", allInfo)
        signalLevel = re.findall("Signal level=(-?\d+?) dBm", allInfo)
        self.listw = []
        result = zip(nameOutput, signalLevel, quality)
        for m in result:
            wm = Wireless()
            wm.setESSID(m[0])
            wm.setSignallevel(m[1])
            wm.setQuality("/".join(m[2]))
            self.listw.append(wm)
        self.updateListView.emit(self.listw)


    def connectedWireLess(self):
        try:
            ipOutput = sp.getoutput("ifconfig wlan0")
            nameOutput = sp.getoutput("iwgetid")
            name = re.findall("ESSID:\"(.*?)\"", nameOutput)
            ip = re.findall(
                "inet (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
                ipOutput)
            uip = ip[0][0] + "." + ip[0][1] + "." + ip[0][2] + "." + ip[0][3]
            self.updateConnectedWifi.emit(name[0],uip)
        except:
            self.updateConnectedWifi.emit("","")


class WirelessModel(QAbstractListModel):
    _connctedIP : str =""
    _connectedSSID : str = ""
    _selectedSSID : str = ""
    _threadScan : QThread

    m_data : [Wireless]

    ESSIDRole = Qt.UserRole
    IPRole = Qt.UserRole + 1
    QualityRole = Qt.UserRole + 2
    SignallevelRole = Qt.UserRole + 3
    IsConnectedRole = Qt.UserRole + 4

    def __init__(self):
        super().__init__()
        self.m_data = []
        # self.allWireless()
        
        self._threadScan = ScannerWorker()
        self._threadScan.updateListView.connect(self.upDateModel)
        self._threadScan.updateConnectedWifi.connect(self.upDateConnectedWifi)
        self._threadScan.start()
        # self.connectedWireLess()
    
    @Slot()
    def threadscanFinished(self):
        self.threadscanerFinished.emit()
    
    @Signal
    def threadscanerFinished(self):
        pass


    @Slot()
    def destroy(self):
        self._threadScan.setFinished(True)
        self._threadScan.wait()
        self._threadScan.quit()


    def rowCount(self, parent) -> int:  ###Override
        if parent.isValid():
            return 0
        return len(self.m_data)

    def data(self, index, role: int) -> Any:  ###Override
        if not index.isValid():
            return
        w = self.m_data[index.row()]
        if role == self.ESSIDRole:
            return w.getESSID()
        elif role == self.IPRole:
            return w.getIP()
        elif role == self.SignallevelRole:
            return w.getSignallevel()
        elif role == self.QualityRole:
            return w.getQuality()
        elif role == self.IsConnectedRole:
            return w.getIsConnect()
        else:
            return None

    def roleNames(self) -> Dict:  ###Override
        default = super().roleNames()
        default[self.ESSIDRole] = QByteArray(b"ESSID")
        default[self.IPRole] = QByteArray(b"IP")
        default[self.QualityRole] = QByteArray(b"Quality")
        default[self.SignallevelRole] = QByteArray(b"Signallevel")
        default[self.IsConnectedRole] = QByteArray(b"IsConnected")
        return default

    def count(self) -> int:
        return len(self.m_data)

    @Signal
    def changed(self):
        pass

    def getConnectedSSID(self):
        return self._connectedSSID

    def setConnectedSSID(self, x):
        self._connectedSSID = x
        self.changed.emit()

    SSID = Property(str, getConnectedSSID, setConnectedSSID, notify=changed)    

    def getConnectedIP(self):
        return self._connctedIP

    def setConnectedIP(self, x):
        self._connctedIP = x
        self.changed.emit()

    IP = Property(str, getConnectedIP, setConnectedIP, notify=changed) 

    def getSelectedSSID(self):
        return self._selectedSSID

    def setSelectedSSID(self, x):
        self._selectedSSID = x
        self.changed.emit()

    SelectedSSID = Property(str, getSelectedSSID, setSelectedSSID, notify=changed)   
    
    
    @Slot(list)
    def upDateModel(self, wifis):
        self.beginResetModel()
        self.m_data = wifis
        self.endResetModel()
    
    @Slot(str,str)
    def upDateConnectedWifi(self,name,ip):
        self.setConnectedIP(ip)
        self.setConnectedSSID(name)
        

    @Slot(str)
    def wifiConfig(self, new_psk:str):
        os.chmod('/etc/wpa_supplicant/wpa_supplicant.conf', stat.S_IRWXU)
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
            old_config = f.readlines()
        ssids = []
        psks = []
        for line in old_config:
            if re.search('.*ssid=(.*?)\n', line) is not None:
                ssids.append(re.search('.*ssid=(.*?)\n', line).group(1)[1:-1])
            if re.search('.*psk=(.*?)\n', line) is not None:
                psks.append(re.search('.*psk=(.*?)\n', line).group(1)[1:-1])

        if self.SelectedSSID not in ssids:
            ssids.append(self.SelectedSSID)
            psks.append(new_psk)
        else:
            psks[ssids.index(self.SelectedSSID)] = new_psk

        config = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
        config.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=IR\n\n")
        for i in range(len(ssids)):
            if ssids[i] == self.SelectedSSID:
                config.write('network={\n' +
                             '\tssid=\"' + ssids[i] + '\"\n' +
                             '\tpsk=\"' + psks[i] + '\"\n' +
                             '\tpriority=' + str(10) +'\n'+
                             '}\n\n')
            else:
                config.write('network={\n' +
                             '\tssid=\"' + ssids[i] + '\"\n' +
                             '\tpsk=\"' + psks[i] + '\"\n' +
                             '\tpriority=' + str(1) +'\n'+
                             '}\n\n')
        config.close()
        sleep(1)
        os.system("sudo wpa_cli -i wlan0 reconfigure")

    @Slot(int)
    def selectedWifi(self,index:int):
        self.setSelectedSSID(self.m_data[index].getESSID())
        # print(self.getSelectedSSID())

    @Slot()
    def closeThread(self):
        self._threadScan.quit()

    @Slot()
    def clearWPASupplicant(self):
        os.chmod('/etc/wpa_supplicant/wpa_supplicant.conf', stat.S_IRWXU)
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as config:
            config.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=IR\n\n")