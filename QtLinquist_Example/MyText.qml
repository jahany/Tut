import QtQuick 2.12

Item {
    id: myitem
    property alias text_property: text1.text
    property alias x_location: text1.x
    property alias y_location: text1.y


    Rectangle {
        color: "transparent"
        width: 200
        height: 200
    }

    Text {
        id: text1
        text: myitem.text_property
        color: "#4455FF"
        font.pixelSize: 30
        x: 0
        y: 0
    }
}
