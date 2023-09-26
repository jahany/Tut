// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Window 2.12
// import akam.binding 1.0

// Window {
//     visible: true
//     width: 400
//     height: 200
//     title: "Product Display"

//     Bindingtest{
//         id:bb
//     }

//     Rectangle {
//         color: "lightgray"
//         anchors.fill: parent

//         Text {
//             id: productLabel
//             text: "Product:" + bb.readedBarcode
//             anchors.centerIn: parent
//             font.pixelSize: 20
//         }
//     }
// }


import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.12
// import akam.binding 1.0
import logic.binding 1.0

Window {
    visible: true
    width: 400
    height: 200
    title: "Product Display"

    // Scanner{
    //     id:bb
    // }

    Logic{
        id:ll
    }

    Rectangle {
        color: "lightgray"
        anchors.fill: parent

        // Text {
        //     id: productLabel
        //     text: "Product:" + bb.read_product
        //     anchors.centerIn: parent
        //     font.pixelSize: 20
        // }

        Text {
            id: sfeqwr
            text: "Product:" + ll.read_product.product_barcode
            anchors.centerIn: parent
            font.pixelSize: 20
        }
    }
}
