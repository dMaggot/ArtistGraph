import artgraph.node

class Relationship():
    _subject = None
    _predicate = None
    
    def __init__(self, subject, predicate):
        self._subject = subject
        self._predicate = predicate
        
    def get_subject(self):
        return self._subject
    
    def get_predicate(self):
        return self._predicate
        
class AssociatedActRelationship(Relationship):
    def __init__(self, subject, predicate):
        Relationship.__init__(self, subject, predicate)
    