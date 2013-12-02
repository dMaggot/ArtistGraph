from artgraph.node import NodeTypes
from artgraph.plugins import Plugin

class DiscographyPlugin(Plugin):
    def __init__(self, node):
        Plugin.__init__(self, node)
        
    @staticmethod
    def get_target_node_type():
        return NodeTypes.ARTIST
        
    def get_nodes(self):
        import re
        from artgraph.node import Node, NodeTypes
        from artgraph.relationship import ArtistAlbumRelationship
        from mwparserfromhell import parse
        
        relationships = []
        node = self.get_node()
        wikicode = self.get_wikicode(node.get_dbtitle())
        list_regexp = re.compile("[#*][\s]+([^\n]+)")
        
        if wikicode:
            for s in wikicode.get_sections(matches="Discography"):
                print s
                for m in list_regexp.findall(str(s)):
                    album_wikicode = parse(m)
                    
                    for w in album_wikicode.filter_wikilinks():
                        relationships.append(ArtistAlbumRelationship(node, Node(str(w.title), NodeTypes.ALBUM)))
                        break
                
        return relationships