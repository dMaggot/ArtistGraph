import QtQuick 1.1

Rectangle {
    color: 'transparent'
    id: graphArea

    function addNode(node) {
        var component = Qt.createComponent("NodeRenderer.qml");

        if (graphArea.children.length > 0) {
            component.createObject(graphArea, { 'node': node, 'x': graphArea.children.length * 100 });
        }
        else {
            var nodeRenderer = component.createObject(graphArea, { 'node': node });

            nodeRenderer.anchors.centerIn = graphArea;
        }
    }
}
