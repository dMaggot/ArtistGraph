class Relationship(object):
    __subject = None
    __predicate = None
    
    def __init__(self, subject, predicate):
        self.__subject = subject
        self.__predicate = predicate
        
    def get_subject(self):
        return self.__subject
    
    def get_predicate(self):
        return self.__predicate
    
    def save(self, cursor):
        pass
    
    def labelsp(self):
        return None
    
    def labelps(self):
        return None
        
class AssociatedActRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
    def save(self, cursor):
        a = self.get_subject().get_id()
        b = self.get_predicate().get_id()
        
        cursor.execute("""
        REPLACE INTO assoc_artist (artistID, assoc_ID)
        VALUES (%s, %s)
        """, (min(a,b), max(a,b)))
        
    def labelsp(self):
        return "Associated to"
    
    def labelps(self):
        return "Associated to"
        
class ArtistGenreRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
    def save(self, cursor):
        cursor.execute("""
        REPLACE INTO `artist_genre` (artistID, genreID)
        VALUES (%s, %s)
        """, (self.get_subject().get_id(), self.get_predicate().get_id()))
        
    def labelsp(self):
        return "Genre is"
    
    def labelps(self):
        return "Representative artist"
        
class MembershipRelationship(Relationship):
    def __init__(self, subject, predicate, current):
        Relationship.__init__(self, subject, predicate)
        self.__current = current
        
    def save(self, cursor):
        a = self.get_subject().get_id()
        b = self.get_predicate().get_id()
        
        cursor.execute("""
        DELETE FROM assoc_artist WHERE (artistID = %(a)s AND assoc_ID = %(b)s) OR (artistID = %(b)s AND assoc_ID = %(a)s)
        """, {'a': a, 'b': b})
        
        cursor.execute("""
        INSERT INTO membership (groupID, artistID, current)
        VALUES (%s, %s, %s)
        """, (a, b, self.__current))
        
    def labelsp(self):
        if self.__current:
            return "Member of"
        else:
            return "Former member of"
        
    def labelps(self):
        if self.__current:
            return "Member"
        else:
            return "Former member"
        
class ArtistAlbumRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
    def save(self, cursor):
        cursor.execute("""
        REPLACE INTO `album_artist` (artistID, albumID)
        VALUES (%s, %s)
        """, (self.get_subject().get_id(), self.get_predicate().get_id()))
        
    def labelsp(self):
        return "Has album"
    
    def labelps(self):
        return "By"
    
class AlbumLabelRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
    def save(self, cursor):
        cursor.execute("""
        UPDATE album SET lableID = %s WHERE id = %s 
        """, (self.get_predicate().get_id(), self.get_subject().get_id()))
        
    def labelsp(self):
        return "Under label"
    
    def labelps(self):
        return "Made album"
        
class SubgenreRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
    def labelsp(self):
        return "Subgenre"
        
    def labelps(self):
        return "Subgenre of"