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
    
    def __init__(self, debug=False):
        mwinterface = pymw.interfaces.GenericInterface()
        self.master = pymw.PyMW_Master(mwinterface, delete_files=not debug)

    def mine(self, artist):
        self.mine_internal(Node(artist, NodeTypes.ARTIST))
        (finished_task, new_relationships) = self.master.get_result()
        
        while new_relationships:
            for n in new_relationships:
                self.relationships.append(n)
                
                if n.get_predicate() not in self.nodes:
                    self.mine_internal(n.get_predicate())
        
    def mine_internal(self, current_node, level=0, parent=None, relationship=None):
        self.nodes.append(current_node)
        
        infoboxplugin = artgraph.plugins.infobox.InfoboxPlugin(current_node)
        self.task_queue.append(self.master.submit_task(infoboxplugin.get_nodes, input_data=(infoboxplugin,), modules=("artgraph",), data_files=("my.cnf",)))
