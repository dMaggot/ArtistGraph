import sys
import thread
import MySQLdb

from PyQt4.QtCore import Qt, QObject, QUrl, pyqtSignal, pyqtProperty
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView

from artgraph.miner import Miner
from artgraph.node import Node, NodeTypes
from artgraph.relationship import *

class NodeWrapper(QObject):
    property_changed = pyqtSignal()
    
    def __init__(self, node, parent=None):
        QObject.__init__(self, parent)
        self.__node = node
        
    def get_node(self):
        return self.__node
        
    @pyqtProperty(int, notify=property_changed)
    def id(self):
        return self.__node.get_id()
    
    @pyqtProperty(str, notify=property_changed)
    def type(self):
        return str(self.__node.get_type())
    
    @pyqtProperty(str, notify=property_changed)
    def name(self):
        return self.__node.get_title()
    
    @pyqtProperty(QUrl, notify=property_changed)
    def image(self):
        image_location = self.get_property('imageLocation')
        
        if image_location:
            return QUrl(image_location)
        else:
            return QUrl()
    
    @pyqtProperty(str, notify=property_changed)
    def realName(self):
        name = self.get_property('name')
        
        if name:
            return name
        else:
            return ""
        
    def get_property(self, property_name):
        db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")
        cursor = db.cursor()
        
        cursor.execute("SELECT %s FROM %s WHERE id = %s" % (property_name, self.get_table_name(), "%s"), (self.__node.get_id(),))
        result = cursor.fetchone()
        db.close()
        
        if result:
            return result[0]
        else:
            return result
    
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
    
    def __init__(self, relationship, current_node, parent=None):
        QObject.__init__(self, parent)
        self.__relationship = relationship
        self.__subject_wrapper = NodeWrapper(relationship.get_subject())
        self.__predicate_wrapper = NodeWrapper(relationship.get_predicate())
        
        if self.__relationship.get_subject().get_id() == current_node.get_id():
            self.__label = self.__relationship.labelsp()
        else:
            self.__label = self.__relationship.labelps()  
     
    @pyqtProperty(NodeWrapper, notify=property_changed) 
    def subject(self):
        return self.__subject_wrapper 
     
    @pyqtProperty(NodeWrapper, notify=property_changed)
    def predicate(self):
        return self.__predicate_wrapper
    
    @pyqtProperty(str, notify=property_changed)
    def label(self):
        return self.__label

class MinerGui(QApplication):
    node_added_signal = pyqtSignal(NodeWrapper)
    node_updated_signal = pyqtSignal(NodeWrapper)
    relationship_added_signal = pyqtSignal(RelationshipWrapper)
    nodeChanged = pyqtSignal(NodeWrapper)
    
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.__miner = Miner()
        self.__current_node = None
        self.__nodewrappers_map = {}
        self.__relationships = []
        self.__is_setup = False
        
        self.setup_view()

        self.aboutToQuit.connect(self.cancel_miner)
        self.node_added_signal.connect(self.node_added)
        self.node_updated_signal.connect(self.node_updated)
        self.relationship_added_signal.connect(self.relationship_added)
        self.nodeChanged.connect(self.query_miner, Qt.QueuedConnection)
        
    def setup_view(self):
        self.__view = QDeclarativeView()
        self.__view.setSource(QUrl('data/main.qml'))
    
        toplevelObject =  self.__view.rootObject()
        toplevelObject.initialArtist.connect(self.start_miner)
        
        self.__view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        self.__view.show()
        
    def cancel_miner(self):
        self.__miner.cancel = True
        
    def start_miner(self, artist):
        thread_args = (artist, self.node_callback, self.relationship_callback)
        self.__thread_id = thread.start_new_thread(self.__miner.mine, thread_args)
        
    def query_miner(self, node_wrapper):
        self.blockSignals(True)
        
        self.__nodewrappers_map = {}
        self.__relationships = []
        self.__is_setup = False
        self.__current_node = node_wrapper.get_node()
        self.__nodewrappers_map[node_wrapper.id] = node_wrapper
        
        self.node_added(node_wrapper)
        self.get_relationships(self.__current_node)
        
        self.blockSignals(False)
        
    def get_relationships(self, node):
        db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")
        cursor = db.cursor()
        
        if node.get_type() == NodeTypes.ARTIST:
            cursor.execute("SELECT albumID, title FROM album_artist INNER JOIN album ON album_artist.albumID = album.id WHERE artistID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ALBUM, ArtistAlbumRelationship, True)
            
            cursor.execute("SELECT artistID, stageName, current FROM membership INNER JOIN artist ON membership.artistID = artist.id WHERE groupID = %s", (node.get_id(),))
            self.wrap_and_add_membership_results(node, cursor, True)
                
            cursor.execute("SELECT artistID, stageName FROM assoc_artist INNER JOIN artist ON assoc_artist.artistID = artist.id WHERE assoc_ID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ARTIST, AssociatedActRelationship, True)
            
            cursor.execute("SELECT groupID, stageName, current FROM membership INNER JOIN artist ON membership.groupID = artist.id WHERE artistID = %s", (node.get_id(),))
            self.wrap_and_add_membership_results(node, cursor, False)
                
            cursor.execute("SELECT assoc_ID, stageName FROM assoc_artist INNER JOIN artist ON assoc_artist.assoc_ID = artist.id WHERE artistID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ARTIST, AssociatedActRelationship, True)
            
            cursor.execute("SELECT genreID, genreName FROM artist_genre INNER JOIN genre ON artist_genre.genreID = genre.id WHERE artistID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.GENRE, ArtistGenreRelationship, True)
        if node.get_type() == NodeTypes.ALBUM:
            cursor.execute("SELECT artistID, stageName FROM album_artist INNER JOIN artist ON album_artist.artistID = artist.id WHERE albumID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ARTIST, ArtistAlbumRelationship, False)
            cursor.execute("SELECT lableID, lableName FROM album INNER JOIN label ON album.lableID = label.ID WHERE album.id = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.LABEL, AlbumLabelRelationship, True)
        if node.get_type() == NodeTypes.GENRE:
            cursor.execute("SELECT artistID, stageName FROM artist_genre INNER JOIN artist ON artist_genre.artistID = artist.id WHERE genreID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ARTIST, ArtistGenreRelationship, False)
        if node.get_type() == NodeTypes.LABEL:
            cursor.execute("SELECT id, title FROM album WHERE lableID = %s", (node.get_id(),))
            self.wrap_and_add_results(node, cursor, NodeTypes.ALBUM, AlbumLabelRelationship, False)
            
                
        db.close()
        
    def wrap_and_add_results(self, node, cursor, node_type, RelationshipClass, direction):
        for r in cursor:
            new_node = Node(r[1], node_type)
            new_node.set_id(r[0])
            
            if direction:
                relationship_wrapper = RelationshipWrapper(RelationshipClass(node, new_node), node, self)
                self.node_added(relationship_wrapper.predicate)
            else:
                relationship_wrapper = RelationshipWrapper(RelationshipClass(new_node, node), node, self)
                self.node_added(relationship_wrapper.subject)
            
            self.relationship_added(relationship_wrapper)
            
    def wrap_and_add_membership_results(self, node, cursor, direction):
        for r in cursor:
            new_node = Node(r[1], NodeTypes.ARTIST)
            new_node.set_id(r[0])
            current = r[2]
            
            if direction:
                relationship_wrapper = RelationshipWrapper(MembershipRelationship(node, new_node, current), node, self)
                self.node_added(relationship_wrapper.predicate)
            else:
                relationship_wrapper = RelationshipWrapper(MembershipRelationship(new_node, node, current), node, self)
                self.node_added(relationship_wrapper.subject)
            
            self.relationship_added(relationship_wrapper)
        
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
            relationship_wrapper = RelationshipWrapper(relationship, self.__current_node)
            
            if (self.__current_node.get_id() <> a) and (a not in self.__nodewrappers_map):
                node_wrapper = relationship_wrapper.subject
                self.__nodewrappers_map[a] = node_wrapper
                self.node_added_signal.emit(node_wrapper)
            elif (self.__current_node.get_id() <> b) and (b not in self.__nodewrappers_map):
                node_wrapper = relationship_wrapper.predicate
                self.__nodewrappers_map[b] = node_wrapper
                self.node_added_signal.emit(node_wrapper)

            self.__relationships.append(relationship_wrapper)
            self.relationship_added_signal.emit(relationship_wrapper)
        
    def node_added(self, node_wrapper):
        if not self.__is_setup:
            self.__view.rootContext().setContextProperty('globalApp', self)
            self.__view.setSource(QUrl('data/graph.qml'))
            self.__is_setup = True
            
        self.__view.rootObject().addNode(node_wrapper)
    
    def node_updated(self, node_wrapper):
        node_wrapper.property_changed.emit()
        
    def relationship_added(self, relationship_wrapper):
        self.__view.rootObject().addRelationship(relationship_wrapper)
        
if __name__ == "__main__":
    app = MinerGui(sys.argv)
    
    sys.exit(app.exec_())
