import sys
import thread
import MySQLdb

from PyQt4.QtCore import QUrl, QObject, pyqtSignal, pyqtProperty
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView

from artgraph.miner import Miner
from artgraph.node import NodeTypes

class NodeWrapper(QObject):
    property_changed = pyqtSignal()
    
    def __init__(self, node, parent=None):
        QObject.__init__(self, parent)
        self.__node = node
        
    @pyqtProperty(int, notify=property_changed)
    def id(self):
        return self.__node.get_id()
    
    @pyqtProperty(str, notify=property_changed)
    def name(self):
        return self.__node.get_title()
    
    @pyqtProperty(str, notify=property_changed)
    def image(self):
        return self.get_property('imageLocation')
    
    @pyqtProperty(str, notify=property_changed)
    def realName(self):
        return self.get_property('name')
        
    def get_property(self, property_name):
        db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")
        cursor = db.cursor()
        
        cursor.execute("SELECT %s FROM %s WHERE artistID = %s" % (property_name, self.get_table_name(), "%s"), (self.__node.get_id(),))
        
        return cursor.fetchone()[0]
    
    def get_table_name(self):
        node_type = self.__node.get_type()
        
        if node_type == NodeTypes.ARTIST:
            return 'artist'
        elif node_type == NodeTypes.ALBUM:
            return 'album'
        elif node_type == NodeTypes.LOCATION:
            return 'location'
        elif node_type == NodeTypes.GENRE:
            return 'genre'
        
class RelationshipWrapper(QObject):
    property_changed = pyqtSignal()
    
    def __init__(self, relationship, parent=None):
        QObject.__init__(self, parent)
        self.__relationship = relationship
        self.__subject_wrapper = NodeWrapper(relationship.get_subject())
        self.__predicate_wrapper = NodeWrapper(relationship.get_predicate())  
     
    @pyqtProperty(NodeWrapper, notify=property_changed)    
    def subject(self):
        return self.__subject_wrapper 
     
    @pyqtProperty(NodeWrapper, notify=property_changed)
    def predicate(self):
        return self.__predicate_wrapper

class MinerGui(QApplication):
    node_added_signal = pyqtSignal(NodeWrapper)
    node_updated_signal = pyqtSignal(NodeWrapper)
    relationship_added_signal = pyqtSignal(RelationshipWrapper)
    
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.__miner = Miner()
        self.__current_node = None
        self.__nodewrappers_map = {}
        self.__is_setup = False
        self.__view = None
        self.aboutToQuit.connect(self.cancel_miner)
        self.node_added_signal.connect(self.node_added)
        self.node_updated_signal.connect(self.node_updated)
        self.relationship_added_signal.connect(self.relationship_added)
        self.relationships = []
        
    def cancel_miner(self):
        self.__miner.cancel = True
        
    def set_view(self, view):
        self.__view = view
        
    def start_miner(self, artist):
        thread_args = (artist, self.node_callback, self.relationship_callback)
        self.__thread_id = thread.start_new_thread(self.__miner.mine, thread_args)
        
    def node_callback(self, node):
        if not self.__current_node:
            self.__current_node = node
            
        if len(self.__nodewrappers_map) == 0:
            wrapper = NodeWrapper(node)
            
            self.__nodewrappers_map[node.get_id()] = wrapper
            self.node_added_signal.emit(wrapper)
        elif node.get_id() in self.__nodewrappers_map:
            self.node_updated_signal.emit(self.__nodewrappers_map[node.get_id()])
        
    def relationship_callback(self, relationship):
        a = relationship.get_subject().get_id()
        b = relationship.get_predicate().get_id()
        
        if self.__current_node.get_id() in [a, b]:
            relationship_wrapper = RelationshipWrapper(relationship)
            
            if self.__current_node.get_id() <> a:
                node_wrapper = relationship_wrapper.subject
                self.__nodewrappers_map[a] = node_wrapper
                self.node_added_signal.emit(node_wrapper)
            elif self.__current_node.get_id() <> b:
                node_wrapper = relationship_wrapper.predicate
                self.__nodewrappers_map[b] = node_wrapper
                self.node_added_signal.emit(node_wrapper)

            self.relationships.append(relationship_wrapper)
            self.relationship_added_signal.emit(relationship_wrapper)
        
    def node_added(self, node_wrapper):
        if not self.__is_setup:
            self.__view.setSource(QUrl('data/graph.qml'))
            self.__is_setup = True
            
        self.__view.rootObject().addNode(node_wrapper)
            
    def node_updated(self, node_wrapper):
        node_wrapper.property_changed.emit()
        
    def relationship_added(self, relationship_wrapper):
        self.__view.rootObject().addRelationship(relationship_wrapper)
        
if __name__ == "__main__":
    app = MinerGui(sys.argv)
    
    # Create the QML user interface.
    view = QDeclarativeView()
    app.set_view(view)
    view.setSource(QUrl('data/main.qml'))
    toplevelObject = view.rootObject()
    toplevelObject.initialArtist.connect(app.start_miner)
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
    
    view.show()
    
    sys.exit(app.exec_())
