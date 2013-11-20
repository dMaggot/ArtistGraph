import artgraph.node

class Relationship():
    __subject = None
    __predicate = None
    
    def __init__(self, subject, predicate):
        self.__subject = subject
        self.__predicate = predicate
        
    def get_subject(self):
        return self.__subject
    
    def get_predicate(self):
        return self.__predicate
        
class AssociatedActRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
class ArtistGenreRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
class ArtistAlbumRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
        
class SubgenreRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)