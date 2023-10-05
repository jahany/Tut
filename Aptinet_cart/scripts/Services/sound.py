from PySide2.QtMultimedia import QMediaPlayer,QMediaContent,QSound


def deleteSound():
    QSound.play("/home/kast/hazf.wav")

def insertSound():
    QSound.play("/home/kast/ezafe.wav")

def notifSound():
    QSound.play("/home/kast/notif.wav")

def notifSound2():
    QSound.play("/home/kast/notif2.wav")
