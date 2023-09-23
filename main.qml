import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import akam.binding 1.1

ApplicationWindow {
    width: 450
    height: 400
    visible: true
    title: "Analog Clock"

    GetTimeOnline {
        id: gto
    }

    Rectangle {
        id: myRec
        color: "red"
        anchors.fill: parent
    }

    MyClock {
        id: cl
        anchors.centerIn: myRec
        hourrotation.angle: (gto.hourProperty * 30) + (gto.minutesProperty * 0.5)
        minuterotation.angle: gto.minutesProperty * 6
        secondrotation.angle: gto.secondsProperty * 6
        hour.source: "assets/hour.png"
        bg.source: "assets/bg.png"
    }

}
