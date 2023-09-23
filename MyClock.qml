import QtQuick 2.12
import akam.binding 1.1


Item {
    id: root
    width: 450
    height: 400

    property alias hourrotation: hourarrowrotation
    property alias minuterotation: minutearrowrotation
    property alias secondrotation: secondarrowrotation
    property alias hour: hourarrow
    property alias bg: bg

    GetTimeOnline {
        id: gto
    }

    Rectangle {
        id: myRec
        color: "transparent"
        anchors.fill: root
        width: root.width
        height: root.height

        Image {
            id: bg
            source: "assets/bg.png"
            visible: true
            anchors.fill: myRec
            width: myRec.width
            height: myRec.height
        }


        Image {
            id: hourarrow
            source: "assets/hour.png"
            visible: true
            x: (bg.width / 2) - 5
            y: (bg.height / 2) - (hourarrow.height / 2) - 25
            transform: Rotation {
                id: hourarrowrotation
                angle: 20
                origin.x: 2
                origin.y: 80
                Behavior on angle {
                    SpringAnimation {
                        id: hourarrowanimation
                        damping: 0.2
                        loops: Animation.Infinite
                        spring: 2
                        modulus: 360
                    }
                }
            }
        }

        Image {
            id: minutearrow
            source: "assets/minute.png"
            visible: true
            x: (bg.width / 2)
            y: (bg.height / 2) - (hourarrow.height / 2) - 20
            transform: Rotation {
                id: minutearrowrotation
                angle: 60
                origin.x: 2
                origin.y:  80
                Behavior on angle {
                    SpringAnimation {
                        id: minutearrowanimation
                        damping: 0.2
                        loops: Animation.Infinite
                        spring: 2
                        modulus: 360
                    }
                }
            }
        }


        Image {
            id: secondarrow
            source: "assets/second.png"
            visible: true
            x: (bg.width / 2) - 5
            y: (bg.height / 2) - (hourarrow.height / 2) - 25
            transform: Rotation {
                id: secondarrowrotation
                angle: 100
                origin.x: 2
                origin.y: 80
                Behavior on angle {
                    SpringAnimation {
                        id: secondarrowanimation
                        damping: 0.2
                        loops: Animation.Infinite
                        spring: 2
                        modulus: 360
                    }
                }
            }
        }
    }
}
