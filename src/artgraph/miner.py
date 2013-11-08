import inspect
import sys

import MySQLdb
import pymw
import pymw.interfaces

import artgraph.plugins
import artgraph.relationship

from artgraph.node import NodeTypes
from artgraph.node import Node

class Miner(object):
    nodes = []
    master = None
    task_queue = []
    db = None
    plugins = {}
    
    def __init__(self, debug=False):
        mwinterface = pymw.interfaces.GenericInterface()
        self.master = pymw.PyMW_Master(mwinterface, delete_files=not debug)
        self.db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")
        
        self.load_plugins(debug)
        
    def load_plugins(self, debug):
        for m in inspect.getmembers(artgraph.plugins, inspect.ismodule):
            for plugin_name, plugin in inspect.getmembers(m[1], lambda (x): inspect.isclass(x) and issubclass(x, artgraph.plugins.Plugin)):
                node_type = plugin.get_target_node_type()
                
                if debug:
                    sys.stderr.write("Loading %s...\n" % plugin_name)
                    
                if node_type:
                    if node_type in self.plugins:
                        self.plugins[node_type].append(plugin)
                    else:
                        self.plugins[node_type] = [plugin]  

    def mine(self, artist):
        first_node = Node(artist, NodeTypes.ARTIST)
        self.add_node(first_node)
        self.mine_internal(first_node)
        (finished_task, new_relationships) = self.master.get_result()
        
        while finished_task:
            for n in new_relationships:
                new_node = n.get_predicate()
                old_nodes = list(x for x in self.nodes if x == new_node)
                
                if len(old_nodes) == 0:
                    self.add_node(new_node)
                    self.mine_internal(new_node)
                else:
                    new_node.set_id(old_nodes[0].get_id())
                
                self.add_relationship(n)
                    
            (finished_task, new_relationships) = self.master.get_result()
            
        self.db.close()
        
    def mine_internal(self, current_node, level=0, parent=None, relationship=None):
        self.nodes.append(current_node)
        
        for p in self.plugins[current_node.get_type()]:
            plugin = p(current_node)
            self.task_queue.append(self.master.submit_task(plugin.get_nodes, input_data=(plugin,), modules=("artgraph",), data_files=("my.cnf",)))
        
    def add_node(self, node):
        cursor = self.db.cursor()
        
        if node.get_type() == NodeTypes.ARTIST:
            cursor.execute("""
            INSERT INTO `artist` (`stageName`)
            VALUES  (%s)
            """, (node.get_title()))
            node.set_id(self.db.insert_id())
        
        cursor.close()
        self.db.commit()
        
    def add_relationship(self, relationship):
        cursor = self.db.cursor()
        a = relationship.get_subject().get_id()
        b = relationship.get_predicate().get_id()
        
        if relationship.__class__ == artgraph.relationship.AssociatedActRelationship:
                cursor.execute("""
                REPLACE INTO assoc_artist (artistID, assoc_ID)
                VALUES (%s, %s)
                """, (min(a,b), max(a,b)))
        
        cursor.close()
        self.db.commit()
