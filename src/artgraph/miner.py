import inspect
import sys

import MySQLdb
import pymw
import pymw.interfaces

import artgraph.plugins

from artgraph.node import NodeTypes
from artgraph.node import Node

class Miner(object):
    nodes = []
    master = None
    db = None
    plugins = {}
    cancel = False
    
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

    def mine(self, artist, node_callback=None, relationship_callback=None):
        first_node = Node(artist, NodeTypes.ARTIST)
        self.add_node(first_node)
        self.mine_internal(first_node, node_callback)
        (finished_task, new_relationships) = self.master.get_result()
        
        while finished_task:
            if node_callback:
                executed_plugin = finished_task.input_data[0]
                
                node_callback(executed_plugin.get_node())
            
            for n in new_relationships:
                new_node = n.get_predicate()
                old_nodes = list(x for x in self.nodes if x == new_node)
                
                if len(old_nodes) == 0:
                    self.add_node(new_node)
                    
                    if not self.cancel:
                        self.mine_internal(new_node, node_callback)
                else:
                    new_node.set_id(old_nodes[0].get_id())
                
                n.save(self.db.cursor())
                
                if relationship_callback:
                    relationship_callback(n)

            (finished_task, new_relationships) = self.master.get_result()
            
        self.db.close()
        
    def mine_internal(self, current_node, callback=None, level=0):
        node_type = current_node.get_type()
        
        self.nodes.append(current_node)
        
        if callback:
            callback(current_node)
        
        if node_type in self.plugins:
            for p in self.plugins[node_type]:
                plugin = p(current_node)
                self.master.submit_task(plugin.get_nodes, input_data=(plugin,), modules=("artgraph",), data_files=("my.cnf",))
        
    def add_node(self, node):
        cursor = self.db.cursor()
        node_type = node.get_type()
        
        if node_type == NodeTypes.ARTIST:
            cursor.execute("""
            INSERT INTO `artist` (`stageName`)
            VALUES  (%s)
            """, (node.get_title()))
        elif node_type == NodeTypes.GENRE:
            cursor.execute("""
            INSERT INTO `genre` (`genreName`)
            VALUES (%s)
            """, (node.get_title()))
        elif node_type == NodeTypes.ALBUM:
            cursor.execute("""
            INSERT INTO `album` (`title`)
            VALUES (%s)
            """, (node.get_title()))
        elif node_type == NodeTypes.LABEL:
            cursor.execute("""
            INSERT INTO `label` (`lableName`)
            VALUES (%s)
            """, (node.get_title()))

        # Assuming all nodes are identified by AUTO_INCREMENT
        node.set_id(self.db.insert_id())
        
        cursor.close()
        self.db.commit()
