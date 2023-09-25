import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Shapes 1.15
import QtQuick.Layouts 1.15
import analog.binding 1.0

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    title: "Analog Clock"

    AnalogClock{
        id:cc
    }

    Rectangle {
        anchors.fill: parent
        color: "white"

        Item {
            id: clockCenter
            anchors.centerIn: parent
            width: 100
            height: 100

            Rectangle {
                anchors.fill: parent
                color: "pink"
                radius: width / 2
            }
        }

        Image {
            id: clock
            source: "file:///home/mahnaz/akam/clock/assets/clock-night.png" 
            width: 300
            height: 300
            anchors.centerIn: clockCenter
            fillMode: Image.PreserveAspectFit

        }

        Image {
            id: hHand
            source: "file:///home/mahnaz/akam/clock/assets/hour.png" 
            width: 80
            height: 80
            // anchors.centerIn: clockCenter
            anchors.horizontalCenter: clockCenter.horizontalCenter
            anchors.verticalCenter: clockCenter.verticalCenter
            fillMode: Image.PreserveAspectFit
            rotation: 90
            transform: Rotation {
                origin.x: 30
                origin.y: 30
                angle: -90 + (cc.read_hour * 360 / 12)
            }
        }

        Image {
            id: minuteHand
            source: "file:///home/mahnaz/akam/clock/assets/minute.png"
            width: 70
            height: 70
            anchors.centerIn: clockCenter
            // anchors.horizontalCenter: parent.horizontalCenter
            // anchors.verticalCenter: clockCenter.verticalCenter
            fillMode: Image.PreserveAspectFit
            rotation: 180
            transform: Rotation {
                origin.x: 35
                origin.y: 47
                angle: (cc.read_minute * 360 / 60)
            }
        }

        Image {
            id: secondHand
            source: "file:///home/mahnaz/akam/clock/assets/second.png"
            width: 70
            height: 70
            anchors.centerIn: clockCenter
            // anchors.horizontalCenter: parent.horizontalCenter
            // anchors.verticalCenter: clockCenter.verticalCenter
            fillMode: Image.PreserveAspectFit
            rotation: 180
            transform: Rotation {
                origin.x: 35
                origin.y: 47
                angle: (cc.read_second * 360 / 60)
            }
        }
    }


}
