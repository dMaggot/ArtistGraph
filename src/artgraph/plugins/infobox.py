from artgraph.node import NodeTypes
from artgraph.plugins import Plugin

class ArtistInfoboxPlugin(Plugin):
    def __init__(self, node):
        Plugin.__init__(self, node)
    
    @staticmethod
    def get_target_node_type():
        return NodeTypes.ARTIST

    def get_nodes(self):
        from bs4 import BeautifulSoup
        from artgraph.node import Node, NodeTypes
        from artgraph.relationship import AssociatedActRelationship, ArtistGenreRelationship
        
        relationships = []
        node = self.get_node()
        wikicode = self.get_wikicode(node.get_dbtitle())
        
        if wikicode:
            for t in wikicode.filter_templates():
                if t.name.matches('Infobox musical artist'):
                    db = self.get_artistgraph_connection()
                    cursor = db.cursor()
                    
                    # Fill in current node info
                    if t.has('birth_name'):
                        name_cleaner = BeautifulSoup(str(t.get('birth_name').value))
                        
                        while name_cleaner.ref:
                            name_cleaner.ref.extract()
                        
                        cursor.execute("UPDATE artist SET name = %s WHERE artistID = %s", (name_cleaner.get_text(), node.get_id()))
                            
                    if t.has('image'):
                        image_cleaner = BeautifulSoup(str(t.get('image').value))
                        image = image_cleaner.get_text()
                        
                        cursor.execute("UPDATE artist SET imageLocation = %s WHERE artistID = %s", (self.resolve_image(image), node.get_id()))
                    
                    db.commit()
                    db.close()
                        
                    if t.has('associated_acts'):
                        associated_acts = t.get('associated_acts')
                        
                        for w in associated_acts.value.filter_wikilinks():
                            relationships.append(AssociatedActRelationship(node, Node(str(w.title), NodeTypes.ARTIST)))
                    
                    if t.has('genre'):
                        genres = t.get('genre')
                         
                        for w in genres.value.filter_wikilinks():
                            relationships.append(ArtistGenreRelationship(node, Node(str(w.title), NodeTypes.GENRE)))
                            
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
        node = self.get_node()
        wikicode = self.get_wikicode(node.get_dbtitle())
          
        if wikicode:
            for t in wikicode.filter_templates():
                if t.name.matches('Infobox music genre'):
                    if t.has('subgenres'):
                        genres = t.get('subgenres')
                           
                        for w in genres.value.filter_wikilinks():
                            relationships.append(SubgenreRelationship(node, Node(str(w.title), NodeTypes.GENRE)))
                              
                    break
                  
        return relationships