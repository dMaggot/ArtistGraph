import MySQLdb
import mwparserfromhell
import sys
import json
import httplib2

class Plugin():
    __node  = None
    
    def __init__(self, node):
        self.__node = node
         
    @staticmethod
    def get_target_node_type():
        return None
    
    def get_node(self):
        return self.__node

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
            return None
        
        return mwparserfromhell.parse(result[0])
    
    def resolve_image(self, image):
        image = "File:%s" % image
        query = httplib2.urllib.urlencode({'action': "query", 'titles': image, 'prop': 'imageinfo', 'iiprop': 'url', 'iiurlwidth': '400px', 'format': 'json'})
        client = httplib2.Http()
        
        # Anything can go wrong from here on
        try:
            request = client.request("http://en.wikipedia.org/w/api.php?%s" % query, headers= {'User-agent': "ArtistGraph Project <den9562@rit.edu>" })
        
            if request[0].status == 200:
                response_object = json.loads(request[1])
            
                for imageid in response_object['query']['pages']: 
                    return response_object['query']['pages'][imageid]['imageinfo'][0]['thumburl']
        except:
            pass
        
        return image
    
    def get_artistgraph_connection(self):
        return MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")

# List available plugin modules here
import infobox
import wikitext