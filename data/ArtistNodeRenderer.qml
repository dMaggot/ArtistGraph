import QtQuick 1.1

Item {
    property variant node

    Column {
        id: layoutColumn
        anchors.centerIn: parent

        Image {
            width: 200
            height: 200
            fillMode: Image.PreserveAspectFit
            source: node.image
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            font.pointSize: 32
            font.weight: Font.Bold
            text: node.name
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            font.pointSize: 24
            text: node.realName
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}