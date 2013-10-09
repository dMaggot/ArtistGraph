import MySQLdb
import mwparserfromhell

class Plugin():

    def get_wikicode(self, title):
        # TODO Make this a conf
        db = MySQLdb.connect(host="localhost", user="root", passwd="", db="BigData")
        cursor = db.cursor()
        cursor.execute("SELECT old_text FROM text INNER JOIN revision ON text.old_id = revision.rev_text_id INNER JOIN page ON revision.rev_page = page.page_id AND page.page_title = %s", (title))
        
        return mwparserfromhell.parse(cursor.fetchone()[0])
