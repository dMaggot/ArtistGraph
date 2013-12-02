import QtQuick 1.1

Rectangle {
    color: 'transparent'
    id: graphArea

    function addNode(node) {
        var component = null;
        var radius = 300.0;

        // We should probably find out how to marshall NodeTypes
        switch(node.type) {
        case "ARTIST":
            component = Qt.createComponent("ArtistNodeRenderer.qml");
            break;
        case "GENRE":
            component = Qt.createComponent("GenreNodeRenderer.qml");
            break;
        case "ALBUM":
            component = Qt.createComponent("AlbumNodeRenderer.qml");
            break;
        }


        if (component != null) {
            if (graphArea.children.length > 0) {
                var nodeRenderer = component.createObject(graphArea, { 'node': node, 'x': graphArea.children.length * 100, 'scale': 0.25 });

                nodeRenderer.anchors.centerIn = graphArea;

                // At this point the list of children is at least 2
                if(graphArea.children.length > 2) {
                    for (var i = 1; i < graphArea.children.length; i++) {
                        graphArea.children[i].anchors.horizontalCenterOffset = Math.cos(2 * (i - 1) * Math.PI / (graphArea.children.length - 1)) * radius;
                        graphArea.children[i].anchors.verticalCenterOffset = Math.sin(2 * (i - 1) * Math.PI / (graphArea.children.length - 1)) * radius;
                    }
                }
                else {
                    graphArea.children[1].anchors.horizontalCenterOffset = radius;
                }
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
