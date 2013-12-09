import QtQuick 1.1

import QtQuick 1.1

Item {
    property variant relationship
    property Item end

    rotation: getSlope(end.x, end.y)
    transformOrigin: Item.Left

    function getSlope(endx, endy)
    {
        var d = Math.atan2(endy - (parent.y + parent.height) / 2, endx - (parent.x + parent.width) / 2) * 180 / Math.PI;

        return d;
    }

    Column {
        property Item end: parent.end

        anchors.centerIn: parent.Center

        Rectangle {
            id: arrow
            color: 'black'
            height: 2
            smooth: true
            width: getWidth(end.x, end.y)
            opacity: 0.5

            function getWidth(endx, endy)
            {
                return Math.sqrt(Math.pow(endx - parent.parent.x, 2) + Math.pow(endy - parent.parent.y, 2)) * 0.8;
            }
        }

        Text {
            text: relationship.label
            anchors.right: arrow.right
            anchors.margins: 10
        }
    }
}
