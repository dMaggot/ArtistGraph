import QtQuick 1.0

Rectangle {
    id: windowRect
    width: 1024
    height: 768
    color: 'silver'

    function addNode(node) {
        graph.addNode(node);
    }

    function addRelationship(relationship) {
        //console.log(relationship);
    }

    GraphRenderer {
        id: graph
        anchors {
            fill: parent
        }
    }
}
