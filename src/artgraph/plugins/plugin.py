import MySQLdb
import mwparserfromhell

class Plugin():
    db = None
    
    def __init__(self):
        # TODO Make this a conf
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="", db="BigData")
        
    def get_wikicode(self, title):
        cursor = self.db.cursor()
        cursor.execute("SELECT old_text FROM text INNER JOIN revision ON text.old_id = revision.rev_text_id INNER JOIN page ON revision.rev_page = page.page_id AND page.page_title = %s", (title))
        
        return mwparserfromhell.parse(cursor.fetchone()[0])
        
