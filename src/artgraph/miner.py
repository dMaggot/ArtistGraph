import MySQLdb
import pymw
import pymw.interfaces

import artgraph.plugins.infobox

from artgraph.node import NodeTypes
from artgraph.node import Node

class Miner(object):
    nodes = []
    relationships = []
    master = None
    task_queue = []
    db = None
    
    def __init__(self, debug=False):
        mwinterface = pymw.interfaces.GenericInterface()
        self.master = pymw.PyMW_Master(mwinterface, delete_files=not debug)
        self.db = MySQLdb.connect(read_default_file="./my.cnf", read_default_group="client_artistgraph")

    def mine(self, artist):
        self.mine_internal(Node(artist, NodeTypes.ARTIST))
        (finished_task, new_relationships) = self.master.get_result()
        
        while new_relationships:
            for n in new_relationships:
                self.relationships.append(n)
                
                if n.get_predicate() not in self.nodes:
                    cursor = self.db.cursor()
                    new_node = n.get_predicate()
                    
                    # For some reason, enum to enum __eq__ is not working here
                    if str(new_node.get_type()) == str(NodeTypes.ARTIST):
                        cursor.execute("""
                        INSERT INTO `artist` (`stageName`)
                        VALUES  (%s)
                        """, (new_node.get_title()))
                        
                    self.db.commit()
                    self.mine_internal(new_node)
                    
            (finished_task, new_relationships) = self.master.get_result()
            
        self.db.close()
        
    def mine_internal(self, current_node, level=0, parent=None, relationship=None):
        self.nodes.append(current_node)
        
        infoboxplugin = artgraph.plugins.infobox.InfoboxPlugin(current_node)
        self.task_queue.append(self.master.submit_task(infoboxplugin.get_nodes, input_data=(infoboxplugin,), modules=("artgraph",), data_files=("my.cnf",)))
