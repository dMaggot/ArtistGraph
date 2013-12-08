import QtQuick 1.0

Rectangle {
    id: graphArea
    width: 1024
    height: 768
    color: 'silver'

    function updateGraph(node) {
        console.log('added ' + node);
    }

    function addNode(node) {
        var component = null;
        var radius = 0.8;

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
            if (nodeGroup.children.length > 0) {
                var nodeRenderer = component.createObject(nodeGroup, { 'node': node, 'scale': 0.25 });

                nodeRenderer.anchors.centerIn = nodeGroup;

                // At this point the children count is at least 2: main node and this new node
                if(nodeGroup.children.length > 2) {
                    for (var i = 1; i < nodeGroup.children.length; i++) {
                        nodeGroup.children[i].anchors.horizontalCenterOffset = Math.cos(2 * (i - 1) * Math.PI / (nodeGroup.children.length - 1)) * radius * (graphArea.width / 2);
                        nodeGroup.children[i].anchors.verticalCenterOffset = Math.sin(2 * (i - 1) * Math.PI / (nodeGroup.children.length - 1)) * radius * (graphArea.height / 2);
                    }
                }
                else {
                    nodeGroup.children[1].anchors.horizontalCenterOffset = radius;
                }
            }
            else {
                var nodeRenderer = component.createObject(nodeGroup, { 'node': node });

                nodeRenderer.anchors.centerIn = nodeGroup
            }
        }
        else {
            console.log("No renderer for node type " + node.type)
        }
    }

    function addRelationship(relationship) {
        var mainNodeID = nodeGroup.children[0].node.id;
        var nodeToSearch = null;

        if (relationship.subject.id === mainNodeID) {
            nodeToSearch = relationship.predicate;
        }
        else if (relationship.predicate.id === mainNodeID) {
            nodeToSearch = relationship.subject;
        }

        if (nodeToSearch) {
            for (var i = 1; i < nodeGroup.children.length; i++) {
                if (nodeGroup.children[i].node === nodeToSearch) {
                    var component = Qt.createComponent("RelationshipRenderer.qml");
                    var relationshipRenderer = component.createObject(relationshipsGroup, { 'end': nodeGroup.children[i], 'relationship': relationship });

                    relationshipRenderer.anchors.centerIn = relationshipsGroup;

                    break;
                }
            }
        }
    }

    Image {
        anchors {
            right: parent.right
            top: parent.top
            margins: 25
        }

        source: 'ArtsitGraph.png'
    }

    Item {
        id: relationshipsGroup
        anchors.fill: parent
    }

    Item {
        id: nodeGroup
        anchors.fill: parent
    }

    MouseArea {
        anchors.fill: parent

        onClicked: {
            console.log('got a click!');
        }
    }
}
