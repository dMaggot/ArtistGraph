import QtQuick 1.1

Item {
    property variant node

    Column {
        id: layoutColumn
        anchors.centerIn: parent

        Text {
            font.pointSize: 32
            font.weight: Font.Bold
            text: node.name
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
