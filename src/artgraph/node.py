from enum import Enum

NodeTypes = Enum('ARTIST', 'DISCOGRAPHY', 'SONG', 'LOCATION')

class Node(object):
    _title = None
    _image = None
    _type = None

    def __init__(self, title, node_type):
        self._title = title
        self._type = node_type
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self._title == other.get_title())
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_title(self):
        return self._title        
        
    def get_type(self):
        return self._type
        