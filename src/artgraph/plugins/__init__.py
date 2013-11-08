import MySQLdb
import mwparserfromhell
import sys

class Plugin():
    _node  = None
    
    def __init__(self, node):
        self._node = node 
    @staticmethod
    def get_target_node_type():
        return None

    def get_wikicode(self, title):
        db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_wikipedia")
        cursor = db.cursor()
        
        cursor.execute("""
        SELECT old_text
        FROM text
        INNER JOIN revision ON text.old_id = revision.rev_text_id
        INNER JOIN page ON revision.rev_page = page.page_id AND page.page_namespace = 0 AND page.page_title = %s""", (title))
        
        result = cursor.fetchone()
        
        db.close()
        
        if not result:
            sys.stderr.write("Dead end at %s\n" % title)
            
            return None
        
        return mwparserfromhell.parse(result[0])
    
    def get_artistgraph_connection(self):
        return MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")

# List available plugin modules here
import infobox