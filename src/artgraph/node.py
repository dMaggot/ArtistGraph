class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
    
NodeTypes = Enum(['ARTIST', 'ALBUM', 'SONG', 'LOCATION', 'GENRE', 'LABEL'])

class Node(object):
    _id = None
    _title = None
    _dbtitle = None
    _image = None
    _type = None

    def __init__(self, title, node_type, dbtitle=None):
        self._title = title
        self._type = node_type
        self._dbtitle = dbtitle
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self._title == other.get_title())
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_title(self):
        return self._title        
        
    def get_type(self):
        return self._type
    
    def get_dbtitle(self):
        if self._dbtitle:
            return self._dbtitle
        else:
            return self._title.replace(" ", "_")
        
    def set_id(self, node_id):
        self._id = node_id
        
    def get_id(self):
        return self._id
        