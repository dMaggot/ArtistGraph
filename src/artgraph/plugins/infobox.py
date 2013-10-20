from artgraph.plugins.plugin import Plugin
from artgraph.node import Node, NodeTypes
from artgraph.relationship import AssociatedActRelationship

class InfoboxPlugin(Plugin):
    def __init__(self, node):
        self._node = node
        
    def get_nodes(self):
        wikicode = self.get_wikicode(self._node.get_title())
        templates = wikicode.filter_templates()
        relationships = []

        for t in templates:
            if t.name.matches('Infobox musical artist'):
                associated_acts = t.get('associated_acts')
                
                for w in associated_acts.value.filter_wikilinks():
                    relationships.append(AssociatedActRelationship(self._node, Node(w.title, NodeTypes.ARTIST)))
                
        return relationships
        