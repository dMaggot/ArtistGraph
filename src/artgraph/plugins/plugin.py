import MySQLdb
import mwparserfromhell

class Plugin():

    def get_wikicode(self, title):
        db = MySQLdb.connect(read_default_file="./my.cnf")
        clean_title = title.replace(" ", "_")
        
        cursor = db.cursor()
        cursor.execute("""
        SELECT old_text
        FROM text
        INNER JOIN revision ON text.old_id = revision.rev_text_id
        INNER JOIN page ON revision.rev_page = page.page_id AND page.page_namespace = 0 AND page.page_title = %s""", (clean_title))
        
        return mwparserfromhell.parse(cursor.fetchone()[0])
