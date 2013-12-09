import QtQuick 1.0

Item {
    id: windowRect
    width: 1024
    height: 768

    signal initialArtist(string artistName)

    Image {
        anchors.fill: parent
        source: 'background.jpg'
        opacity: 0.5
    }

    Image {
        anchors {
            right: parent.right
            top: parent.top
            margins: 25
        }

        source: 'ArtsitGraph.png'
    }


    Column {
        anchors.centerIn: parent

        Text {
            font.pointSize: 24
            text: 'Input your favorite artist'
            anchors.horizontalCenter: parent.horizontalCenter
        }

        TextInput {
            width: 500
            fillColor: 'white'
            horizontalAlignment: TextInput.AlignHCenter
            font.pointSize: 32
            anchors.horizontalCenter: parent.horizontalCenter
            onAccepted: {
                windowRect.initialArtist(text)
            }
        }
    }
}
