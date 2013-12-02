import QtQuick 1.1

Rectangle {
    color: 'transparent'
    id: graphArea

    function addNode(node) {
        var component = null;

        // We should probably find out how to marshall NodeTypes
        switch(node.type) {
        case "ARTIST":
            component = Qt.createComponent("ArtistNodeRenderer.qml");
            break;
        case "GENRE":
            component = Qt.createComponent("GenreNodeRenderer.qml");
            break;
        }


        if (component != null) {
            if (graphArea.children.length > 0) {
                component.createObject(graphArea, { 'node': node, 'x': graphArea.children.length * 100 });
            }
            else {
                var nodeRenderer = component.createObject(graphArea, { 'node': node });

                nodeRenderer.anchors.centerIn = graphArea;
            }
        }
        else {
            console.log("No renderer for node type " + node.type)
        }
    }
}
