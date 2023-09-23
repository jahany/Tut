import QtQuick 2.15
import QtQuick.Controls 2.15
import akam.binding 1.0

ApplicationWindow {
    id: app
    visible: true
    width: 600
    height: 600
    title: "Product Display"

    Logic_Class {
        id: logicClass
    }

    Rectangle {
        color: "lightblue"
        anchors.fill: parent

        Text {
            id: productQRCode
            text: "QR Code:" + logicClass.productProperty.QRCodeProperty
            x: 220
            y: 50
            font.pixelSize: 30
            font.italic: true
            color: "#3D6D38"
        }

        Text {
            id: productName
            text: "Product:" + logicClass.productProperty.productNameProperty
            x: 220
            y: 150
            font.pixelSize: 30
            font.italic: true
            color: "#6D386A"
        }

        Image {
            id: productImage
            source: logicClass.productProperty.productPhotoProperty
            width: 300
            fillMode: Image.PreserveAspectFit
            opacity: 1
            x: app.width / 4
            y: app.height / 2.5
        }

}
}