import QtQuick 1.1

Item {
    property variant node

    Behavior on anchors.horizontalCenterOffset {
        PropertyAnimation {}
    }

    Behavior on anchors.verticalCenterOffset {
        PropertyAnimation {}
    }

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
