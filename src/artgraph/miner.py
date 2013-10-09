import pymw
import pymw.interfaces


from exceptions import Exception

import plugins.infobox

from node import NodeTypes
from node import Node

class Miner(object):
    nodes = []
    relationships = []
    master = None
    task_queue = []
    
    def __init__(self):
        mwinterface = pymw.interfaces.GenericInterface()
        self.master = pymw.PyMW_Master(mwinterface)

    def mine(self, artist):
        self.mine_internal(Node(artist, NodeTypes.ARTIST))
        new_relationships = self.master.get_result()
        
        while new_relationships:
            for n in new_relationships:
                self.relationships.append(n)
                
                if n.get_predicate() not in self.nodes:
                    self.mine_internal(n.get_predicate())
            
        
    def mine_internal(self, current_node, level=0, parent=None, relationship=None):
        self.nodes.append(current_node)
        
        infoboxplugin = plugins.infobox.InfoboxPlugin(current_node)
        self.task_queue.append(self.master.submit_task(infoboxplugin.get_nodes, input_data=(infoboxplugin), modules=("artgraph.plugins.infobox",)))

        
        
        
