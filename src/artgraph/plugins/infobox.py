from artgraph.node import NodeTypes
from artgraph.plugins import Plugin

class ArtistInfoboxPlugin(Plugin):
    def __init__(self, node):
        Plugin.__init__(self, node)
    
    @staticmethod
    def get_target_node_type():
        return NodeTypes.ARTIST

    def get_nodes(self):
        from artgraph.node import Node, NodeTypes
        from artgraph.relationship import AssociatedActRelationship, ArtistGenreRelationship
        
        relationships = []
        wikicode = self.get_wikicode(self._node.get_dbtitle())
        
        if wikicode:
            for t in wikicode.filter_templates():
                if t.name.matches('Infobox musical artist'):
                    # Fill in current node info
                    if t.has('birth_name'):
                        name = str(t.get('birth_name').value)
                    
                        db = self.get_artistgraph_connection()
                        cursor = db.cursor()
                        cursor.execute("UPDATE artist SET name = %s WHERE artistID = %s", (name, self._node.get_id()))
                        db.commit()
                        db.close()
                    
                    if t.has('associated_acts'):
                        associated_acts = t.get('associated_acts')
                        
                        for w in associated_acts.value.filter_wikilinks():
                            relationships.append(AssociatedActRelationship(self._node, Node(str(w.title), NodeTypes.ARTIST)))
                    
                    if t.has('genre'):
                        genres = t.get('genre')
                         
                        for w in genres.value.filter_wikilinks():
                            relationships.append(ArtistGenreRelationship(self._node, Node(str(w.title), NodeTypes.GENRE)))
                            
                    break
                
        return relationships

class GenreInfoboxPlugin(Plugin):
    def __init__(self, node):
        Plugin.__init__(self, node)
      
    @staticmethod
    def get_target_node_type():
        return NodeTypes.GENRE
      
    def get_nodes(self):
        from artgraph.node import Node, NodeTypes
        from artgraph.relationship import SubgenreRelationship
        
        relationships = []
        wikicode = self.get_wikicode(self._node.get_dbtitle())
          
        if wikicode:
            for t in wikicode.filter_templates():
                if t.name.matches('Infobox music genre'):
                    if t.has('subgenres'):
                        genres = t.get('subgenres')
                           
                        for w in genres.value.filter_wikilinks():
                            relationships.append(SubgenreRelationship(self._node, Node(str(w.title), NodeTypes.GENRE)))
                              
                    break
                  
        return relationships