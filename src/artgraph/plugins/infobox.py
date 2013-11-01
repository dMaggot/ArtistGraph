from artgraph.plugins.plugin import Plugin

class InfoboxPlugin(Plugin):
    def __init__(self, node):
        self._node = node
        
    def get_nodes(self):
        from artgraph.node import Node, NodeTypes
        from artgraph.relationship import AssociatedActRelationship
        
        relationships = []
        wikicode = self.get_wikicode(self._node.get_dbtitle())
        
        if wikicode:
            templates = wikicode.filter_templates()

            for t in templates:
                if t.name.matches('Infobox musical artist'):
                    # Fill in current node info
                    if t.has('birth_name'):
                        name = str(t.get('birth_name').value)
                    
                        db = self.get_artistgraph_connection()
                        cursor = db.cursor()
                        cursor.execute("UPDATE artist SET fName = %s WHERE artistID = %s", (name, self._node.get_id()))
                        db.commit()
                        db.close()
                    
                    associated_acts = t.get('associated_acts')
                
                    for w in associated_acts.value.filter_wikilinks():
                        relationships.append(AssociatedActRelationship(self._node, Node(str(w.title), NodeTypes.ARTIST)))
                
        return relationships
        