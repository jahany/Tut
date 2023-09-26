import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.LocalStorage 2.0
import Qt.labs.settings 1.0
import akam.binding 1.0


Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Multi Language")
    id: root

    Controller {
        id: controller
    }


    Rectangle{
        id: myrect
        width: root.width
        height: root.height
        anchors.fill: root
        color: "#D0FF23"
    }

    MyText {
        id: hellotext
        text_property: qsTr("hello")
        x_location: 100
        y_location: 50

    }

    MyText{
        text_property: qsTr("bye")
        x_location: 100
        y_location: 150
    }

    MyText{
        text_property: qsTr("good")
        x_location: 100
        y_location: 250
    }

    MyText{
        text_property: qsTr("how")
        x_location: 400
        y_location: 50
    }

    MyText{
        text_property: qsTr("why")
        x_location: 400
        y_location: 150
    }

    MyText{
        text_property: qsTr("where")
        x_location: 400
        y_location: 250
    }

    Button{
        id: enbutton
        text: "en"
        font.italic: true
        font.pixelSize: 20
        x: 400
        y: 350
        onClicked: controller.languageProperty = "es"

    }

    Button{
        id: fabutton
        text: "fa"
        font.italic: true
        font.pixelSize: 20
        x: 100
        y: 350
        onClicked: {
            controller.setLanguage("fa")
            controller.languageProperty = "fa"
        }

    }

    Button{
        id: esbutton
        text: "es"
        font.italic: true
        font.pixelSize: 20
        x: 250
        y: 350
        onClicked: {
//            esbutton.text = "dfcds" //just a test to see if onClicked works
            controller.languageProperty = "es"
            controller.setLanguage("es")
        }

    }



}



